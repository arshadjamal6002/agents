import streamlit as st
import requests
import os
import json
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent AI Playground",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title ---
st.title("🧠 Multi-Agent AI Playground")
st.caption("A web interface to interact with a powerful, multi-agent backend.")

# --- API Configuration ---
API_URL = os.getenv("API_URL", "http://localhost:8000")

# --- Helper Functions ---
def get_agents():
    """Fetches agent details from the API."""
    try:
        response = requests.get(f"{API_URL}/agents")
        response.raise_for_status()
        agents_list = response.json()
        agent_map = {agent['name']: agent for agent in agents_list}
        agent_map["Auto (Orchestrator)"] = {
            "name": "Auto (Orchestrator)",
            "description": "Let the orchestrator choose the best agent.",
            "required_inputs": [] # Empty list = single text input
        }
        return agent_map
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Error: {e}")
        return {}

def format_recursively(data, context):
    """Recursively formats strings in a nested data structure."""
    if isinstance(data, dict):
        return {k: format_recursively(v, context) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_recursively(item, context) for item in data]
    elif isinstance(data, str):
        placeholders = re.findall(r"\{\{(.*?)\}\}", data)
        for placeholder in placeholders:
            if placeholder in context:
                data = data.replace(f"{{{{{placeholder}}}}}", str(context.get(placeholder, '')))
        return data
    else:
        return data

# Load Agents (No cache to ensure updates are seen)
AVAILABLE_AGENTS = get_agents()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "custom_prompts" not in st.session_state:
    st.session_state.custom_prompts = {}
if 'chain' not in st.session_state:
    st.session_state.chain = []

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    chaining_mode = st.checkbox("🔗 Enable Agent Chaining", value=False)
    st.markdown("---")
    
    # SINGLE AGENT SELECTOR
    st.header("Mode Selection")
    agent_names = list(AVAILABLE_AGENTS.keys())
    # Default to Orchestrator if available, else first agent
    default_index = agent_names.index("Auto (Orchestrator)") if "Auto (Orchestrator)" in agent_names else 0
    agent_choice = st.selectbox("Choose an agent:", agent_names, index=default_index, disabled=chaining_mode)
    
    # Show info box
    if agent_choice and agent_choice in AVAILABLE_AGENTS:
        info = AVAILABLE_AGENTS[agent_choice]
        reqs = info.get("required_inputs", [])
        if reqs:
            st.info(f"**Inputs:** `{', '.join(reqs)}`")

    st.markdown("---")
    
    # Prompt Editor
    st.header("🛠️ Prompt Editor")
    editable_agents = [name for name in agent_names if name != "Auto (Orchestrator)"]
    selected_for_edit = st.selectbox("Edit prompt for agent:", editable_agents)
    
    existing_prompt = st.session_state.custom_prompts.get(selected_for_edit, "")
    edited_prompt = st.text_area("Custom Prompt:", value=existing_prompt, height=150, key=f"editor_{selected_for_edit}")

    if st.button("💾 Save Prompt"):
        st.session_state.custom_prompts[selected_for_edit] = edited_prompt
        st.success(f"Saved!")

# --- Main Content Area ---
st.header("Your Request")

# We will collect inputs in this dictionary
execution_inputs = {}
file_content = None

# ==========================================
# UI LOGIC: CHAINING MODE
# ==========================================
if chaining_mode:
    st.info("🔗 **Chaining Mode Active**")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        chain_options = [n for n in agent_names if n != "Auto (Orchestrator)"]
        agent_to_add = st.selectbox("Select agent to add:", chain_options, key="chain_add_select")
    with col2:
        if st.button("➕ Add Step", use_container_width=True):
            st.session_state.chain.append({"agent_name": agent_to_add, "inputs": {}})
            st.rerun()

    if st.session_state.chain:
        st.markdown("---")
        for i, step in enumerate(st.session_state.chain):
            agent_name = step['agent_name']
            with st.container(border=True):
                st.subheader(f"Step {i+1}: {agent_name}")
                
                agent_config = AVAILABLE_AGENTS.get(agent_name, {})
                required_inputs = agent_config.get('required_inputs', [])
                
                # Dynamic inputs for Chain Steps
                if required_inputs:
                    for req_input in required_inputs:
                        key = f"chain_input_{i}_{req_input}"
                        val = st.text_area(f"Input for `{req_input}`:", key=key, height=100)
                        step['inputs'][req_input] = val
                else:
                    key = f"chain_input_{i}_raw"
                    val = st.text_area(f"Input for `{agent_name}`:", key=key, height=100)
                    step['inputs']['input'] = val

        if st.button("🗑️ Clear Chain"):
            st.session_state.chain = []
            st.rerun()
            
    # Initial input for the start of the chain
    st.markdown("### Initial Data")
    execution_inputs["initial_input"] = st.text_area("Enter initial prompt / data:", height=100, key="chain_initial_input")

# ==========================================
# UI LOGIC: SINGLE AGENT MODE
# ==========================================
else:
    current_agent_config = AVAILABLE_AGENTS.get(agent_choice, {})
    required_inputs = current_agent_config.get("required_inputs", [])

    # CASE A: Agent has specific required inputs (e.g. resume_analyzer, sql_generator)
    if required_inputs and len(required_inputs) > 0:
        st.subheader(f"Inputs for `{agent_choice}`")
        for req_input in required_inputs:
            # Create a separate text box for each requirement
            execution_inputs[req_input] = st.text_area(f"Enter `{req_input}`:", height=150)
            
    # CASE B: Agent takes a single generic input (Orchestrator)
    else:
        execution_inputs["input"] = st.text_area("Enter your prompt:", height=150)

# Global File Uploader (Available in all modes)
file_upload = st.file_uploader("Or upload a file (content will be added to inputs):", type=["txt", "md", "py", "json", "pdf"])


# ==========================================
# EXECUTION LOGIC
# ==========================================
if st.button("🚀 Run", type="primary"):
    
    # Handle File Upload
    if file_upload:
        try:
            file_content = file_upload.read().decode("utf-8")
            # If we are in single input mode, append file content
            if "input" in execution_inputs:
                execution_inputs["input"] += f"\n\n[File Content]:\n{file_content}"
            # If we are in structured mode, user can decide where to put it, 
            # OR we can just add it to a generic 'file_content' key if needed.
            # For now, let's auto-fill 'pdf_path' or similar if it matches.
        except Exception:
            st.error("Could not read file. Ensure it is text-based.")

    with st.spinner("Processing..."):
        
        # --- PATH A: CHAIN EXECUTION ---
        if chaining_mode and st.session_state.chain:
            context = {"initial_input": execution_inputs.get("initial_input", "")}
            if file_content: context["file_content"] = file_content
            
            final_output = None
            chain_failed = False
            
            for i, step in enumerate(st.session_state.chain):
                agent_name = step['agent_name']
                
                # Format inputs
                raw_inputs = step.get('inputs', {})
                formatted_inputs = format_recursively(raw_inputs, context)
                
                with st.status(f"Running Step {i+1}: {agent_name}...", expanded=True) as status:
                    st.write("**Inputs:**", formatted_inputs)
                    
                    try:
                        payload = {"input": formatted_inputs}
                        if agent_name in st.session_state.custom_prompts:
                            payload["prompt_override"] = st.session_state.custom_prompts[agent_name]

                        res = requests.post(f"{API_URL}/agent/{agent_name}", json=payload)
                        
                        if res.status_code == 200:
                            result = res.json().get("output", res.text)
                            st.write("**Output:**", result)
                            status.update(label=f"✅ Step {i+1} Complete", state="complete", expanded=False)
                            context[f"step_{i+1}_output"] = result
                            final_output = result
                        else:
                            status.update(label="❌ Failed", state="error")
                            st.error(res.text)
                            chain_failed = True
                            break
                    except Exception as e:
                        st.error(f"Connection Error: {e}")
                        chain_failed = True
                        break
            
            if not chain_failed and final_output:
                st.success("Chain Complete!")
                st.session_state.chat_history.append({"agent": "Agent Chain", "input": "Chain Execution", "output": final_output})

        # --- PATH B: SINGLE AGENT EXECUTION ---
        else:
            selected_agent = agent_choice if agent_choice != "Auto (Orchestrator)" else None
            endpoint = f"{API_URL}/agent/{selected_agent}" if selected_agent else f"{API_URL}/instruct"
            
            # Prepare Payload
            # If we collected multiple inputs (structured), send them as a dictionary
            if len(execution_inputs) > 1 or (len(execution_inputs) == 1 and "input" not in execution_inputs):
                payload = {"input": execution_inputs}
            else:
                # Simple single string input
                payload = {"input": execution_inputs.get("input", "")}

            # Prompt Override
            if selected_agent and selected_agent in st.session_state.custom_prompts:
                payload["prompt_override"] = st.session_state.custom_prompts[selected_agent]

            try:
                res = requests.post(endpoint, json=payload)
                if res.status_code == 200:
                    result = res.json().get("output", res.text)
                    st.success("Done!")
                    st.subheader("Result:")
                    
                    if isinstance(result, (dict, list)):
                        st.json(result)
                    else:
                        st.markdown(result)
                    
                    st.session_state.chat_history.append({"agent": agent_choice, "input": payload["input"], "output": result})
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- Chat History ---
st.divider()
if st.session_state.chat_history:
    st.header("📜 History")
    for item in reversed(st.session_state.chat_history):
        with st.expander(f"{item['agent']}"):
            st.write("**Input:**", item['input'])
            st.write("**Output:**", item['output'])
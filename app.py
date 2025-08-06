# ui.py

import streamlit as st
import requests
import os
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent AI Playground",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title ---
st.title("🧠 Multi-Agent AI Playground")

# --- API and Agent Configuration ---
API_URL = os.getenv("API_URL", "http://localhost:8000")

@st.cache_data(ttl=3600)
def get_agents():
    """Fetches the list of available agents from the API."""
    try:
        response = requests.get(f"{API_URL}/agents")
        response.raise_for_status()
        # Fetch the full agent objects
        agents = response.json() 
        # Create a dictionary for easy lookup
        agent_map = {agent['name']: agent for agent in agents}
        # Add the orchestrator as a special case
        agent_map["Auto (Orchestrator)"] = {"name": "Auto (Orchestrator)", "required_inputs": ["A natural language prompt."]}
        return agent_map
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"API Error: {e}")
        return ["Auto (Orchestrator)"]

AVAILABLE_AGENTS = get_agents()

# --- Initialize Session State ---
# This is where we store data that persists across user interactions.
# Enhancement 1: Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Enhancement 2: Custom Prompts
if "custom_prompts" not in st.session_state:
    st.session_state.custom_prompts = {}

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # --- Enhancement 3: Agent Chaining Toggle ---
    st.markdown("---")
    chaining_mode = st.checkbox("🔗 Enable Agent Chaining", value=False)
    st.markdown("---")

    # Original agent selection (moved to sidebar)
    # ui.py sidebar section
    st.header("Agent Selection")

    # The keys of the map are the names for the dropdown
    agent_choice = st.selectbox(
        "Choose an agent to interact with:",
        list(AVAILABLE_AGENTS.keys()),
        disabled=chaining_mode
    )

    # Display the required inputs for the selected agent
    if agent_choice:
        selected_agent_info = AVAILABLE_AGENTS[agent_choice]
        inputs = selected_agent_info.get("required_inputs", [])
        if inputs:
            st.info(f"**Required Inputs:** `{', '.join(inputs)}`")

    # --- Enhancement 2: Prompt Editor ---
    st.title("🛠️ Prompt Editor")
    st.caption("Fine-tune agent behavior for this session.")

    # Exclude "Auto" and "workflow_agent" from being editable
    editable_agents = [agent for agent in AVAILABLE_AGENTS if agent not in ["Auto (Orchestrator)", "workflow_agent"]]
    selected_for_edit = st.selectbox("Edit prompt for agent:", editable_agents)

    # Define some reasonable default prompts
    default_prompts = {
        "resume_analyzer_agent": "Analyze this resume against the job description, providing a match score and suggestions.",
        "email_generator_agent": "You are a professional email writing assistant. Write an email based on the provided context.",
        # Add other default prompts as needed
    }

    # Load existing prompt from session state or default
    existing_prompt = st.session_state.custom_prompts.get(selected_for_edit, default_prompts.get(selected_for_edit, "No default prompt set for this agent."))
    edited_prompt = st.text_area("Custom Prompt:", value=existing_prompt, height=200)

    if st.button("💾 Save Prompt"):
        st.session_state.custom_prompts[selected_for_edit] = edited_prompt
        st.success(f"Custom prompt for {selected_for_edit} saved for this session.")

# --- Main Page Layout ---
st.header("Your Request")

# --- Enhancement 3: UI for Agent Chaining ---
if chaining_mode:
    st.info("🔗 Chaining Mode Enabled: The output of each agent will be the input for the next.")
    selected_chain = st.multiselect(
        "Select agents to chain (in order of execution):",
        [agent for agent in AVAILABLE_AGENTS if agent != "Auto (Orchestrator)"]
    )

# Main input area
user_input = st.text_area("Enter your prompt or data:", height=150)
file_upload = st.file_uploader("Or upload a file (optional):", type=["txt", "md", "py", "json"])

if st.button("🚀 Run"):
    content = user_input
    if file_upload:
        content = file_upload.read().decode("utf-8")

    if not content:
        st.warning("Please provide an input.")
    else:
        # --- Main Execution Logic ---
        with st.spinner("The agents are collaborating..."):
            final_output = None
            
            # --- Enhancement 3: Chaining Logic ---
            if chaining_mode and selected_chain:
                try:
                    chain_input = json.loads(content)
                except json.JSONDecodeError:
                    chain_input = content
                # --- END: THE FIX ---

                for agent_name in selected_chain:
                    with st.expander(f"Step {selected_chain.index(agent_name) + 1}: Running `{agent_name}`", expanded=True):
            # ... loop continues
                        st.markdown(f"**Input:**\n```\n{str(chain_input)[:1000]}...\n```")
                        
                        payload = {"input": chain_input}
                        if agent_name in st.session_state.custom_prompts:
                            payload["prompt_override"] = st.session_state.custom_prompts[agent_name]

                        endpoint = f"{API_URL}/agent/{agent_name}"
                        res = requests.post(endpoint, json=payload)

                        if res.status_code == 200:
                            output = res.json().get("output", res.text)
                            st.markdown("**Output:**")
                            st.json(output) if isinstance(output, (dict, list)) else st.markdown(output)
                            chain_input = output # Pass output to the next agent
                        else:
                            st.error(f"Agent `{agent_name}` failed: {res.text}")
                            chain_input = None
                            break
                final_output = chain_input
            
            # --- Original Single-Agent/Orchestrator Logic ---
            else:
                selected_agent = agent_choice if agent_choice != "Auto (Orchestrator)" else None
                endpoint = f"{API_URL}/agent/{selected_agent}" if selected_agent else f"{API_URL}/instruct"
                
                payload = {"input": content}
                if selected_agent and selected_agent in st.session_state.custom_prompts:
                    payload["prompt_override"] = st.session_state.custom_prompts[selected_agent]
                
                res = requests.post(endpoint, json=payload)

                if res.status_code == 200:
                    result_data = res.json()
                    final_output = result_data.get("output", result_data)
                    st.success("✅ Done!")
                    st.subheader("🧠 Response")
                    st.json(final_output) if isinstance(final_output, (dict, list)) else st.markdown(final_output)
                else:
                    st.error(f"❌ Error: {res.text}")

            # --- Enhancement 1: Append to Chat History ---
            if final_output:
                st.session_state.chat_history.append({
                    "agent": "Agent Chain" if chaining_mode and selected_chain else agent_choice,
                    "input": content,
                    "output": final_output
                })

# --- Enhancement 1: Display Chat History ---
st.divider()
st.header("📜 Chat History")

if not st.session_state.chat_history:
    st.info("Your previous results will appear here.")

for i, msg in enumerate(reversed(st.session_state.chat_history)):
    agent_name = msg.get('agent', 'Unknown')
    with st.expander(f"**{agent_name}** (Run #{len(st.session_state.chat_history) - i})"):
        st.caption("Input:")
        st.code(msg["input"], language="text")
        st.caption("Output:")
        output = msg["output"]
        st.json(output) if isinstance(output, (dict, list)) else st.markdown(output)
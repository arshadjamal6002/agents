# ui.py

import streamlit as st
import requests
import os
from graphviz import Digraph

def render_workflow_graph(agent_list):
    dot = Digraph()
    dot.attr(rankdir="LR", size="8,4")
    
    # Input node
    dot.node("User", shape="ellipse", style="filled", fillcolor="#e0f7fa")
    
    prev = "User"
    for i, agent in enumerate(agent_list):
        node_id = f"{agent}"
        dot.node(node_id, shape="box", style="filled", fillcolor="#ffe0b2")
        dot.edge(prev, node_id)
        prev = node_id

    # Final output
    dot.node("Output", shape="ellipse", style="filled", fillcolor="#c8e6c9")
    dot.edge(prev, "Output")
    return dot


st.set_page_config(page_title="Multi-Agent GenAI System", layout="centered")

st.sidebar.markdown("---")
chaining_mode = st.sidebar.checkbox("🔗 Enable Agent Chaining")


st.title("🧠 Multi-Agent AI System")
st.caption("Interact with any agent or let the orchestrator auto-select.")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Load available agents
AGENTS = ["Auto (Orchestrator)", "summarizer_agent", "code_explainer_agent", "resume_analyzer_agent", "email_writer_agent", "translator_agent"]







st.sidebar.title("🛠️ Prompt Editor")

if "custom_prompts" not in st.session_state:
    st.session_state.custom_prompts = {}

selected_for_edit = st.sidebar.selectbox("Edit prompt for agent:", AGENTS[1:])  # exclude "Auto"

default_prompts = {
    "summarizer_agent": "You are a summarizer. Summarize the input text clearly.",
    "code_explainer_agent": "Explain the following code snippet step by step.",
    "resume_analyzer_agent": "Analyze this resume for strengths and suggest improvements.",
    "email_writer_agent": "Write a professional email based on the following input.",
    "translator_agent": "Translate the following text to English."
}

existing = st.session_state.custom_prompts.get(selected_for_edit) or default_prompts.get(selected_for_edit, "")
edited_prompt = st.sidebar.text_area("Custom Prompt", value=existing, height=200)

if st.sidebar.button("💾 Save Prompt"):
    st.session_state.custom_prompts[selected_for_edit] = edited_prompt
    st.sidebar.success("Custom prompt saved.")











agent_choice = st.selectbox("Select Agent", AGENTS)
user_input = st.text_area("Enter your input:", height=150)

file_upload = st.file_uploader("Or upload a file", type=["txt", "md", "py", "pdf"])






if chaining_mode:
    st.markdown("### 🔁 Agent Chain Execution")
    selected_agents = st.multiselect("Select agents to chain (in order):", AGENTS[1:])  # Exclude Orchestrator











if st.button("🔍 Run"):
    if not user_input and not file_upload:
        st.warning("Please enter some text or upload a file.")
    else:
        content = user_input
        if file_upload:
            content = file_upload.read().decode("utf-8")

        if chaining_mode and selected_agents:
            st.markdown("### 🧠 Workflow Preview")
            st.graphviz_chart(render_workflow_graph(selected_agents))
            # Chaining logic
            chain_input = content
            for agent in selected_agents:
                st.markdown(f"##### 🧠 Agent: `{agent}`")
                payload = {"input": chain_input}

                if agent in st.session_state.custom_prompts:
                    payload["prompt"] = st.session_state.custom_prompts[agent]

                endpoint = f"{API_URL}/agent/{agent}"
                res = requests.post(endpoint, json=payload)

                if res.status_code == 200:
                    output = res.json().get("output", "")
                    st.text_area("Output", value=output, height=150)
                    chain_input = output  # Pass to next agent
                else:
                    st.error(f"❌ Agent `{agent}` failed: {res.text}")
                    break
        else:
    # Single agent or orchestrator mode (already exists)
 
                

            selected_agent = agent_choice if agent_choice != "Auto (Orchestrator)" else None
            endpoint = f"{API_URL}/agent/{selected_agent}" if selected_agent else f"{API_URL}/instruct"

            with st.spinner("Processing..."):
                payload = {"input": content}

                # If specific agent selected, include custom prompt (if any)
                if selected_agent and selected_agent in st.session_state.custom_prompts:
                    payload["prompt"] = st.session_state.custom_prompts[selected_agent]

                res = requests.post(endpoint, json=payload)

                if res.status_code == 200:
                    result = res.json().get("output", res.text)
                    st.success("✅ Done")
                    st.text_area("🧠 Response", value=result, height=200)
                else:
                    st.error("❌ Error: " + res.text)

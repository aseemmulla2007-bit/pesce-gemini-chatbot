import streamlit as st
import os
import time

try:
    from google import genai
except ImportError:
    import google.genai as genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="PESCE Elite Assistant", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-base:        #F7F8FC;
        --bg-surface:     #FFFFFF;
        --bg-user-bubble: #EEF2FF;
        --bg-ai-bubble:   #FFFFFF;
        --accent:         #4F6EF7;
        --accent-glow:    rgba(79, 110, 247, 0.18);
        --accent-soft:    rgba(79, 110, 247, 0.08);
        --border:         rgba(79, 110, 247, 0.15);
        --text-primary:   #1A1D2E;
        --text-secondary: #5A5E7A;
        --text-placeholder: #9CA3C0;
        --shadow-card:    0 2px 16px rgba(79,110,247,0.08), 0 1px 4px rgba(0,0,0,0.05);
        --shadow-glow:    0 0 0 3px var(--accent-glow);
        --radius-bubble:  18px;
        --radius-input:   14px;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg-base:        #0D0F1A;
            --bg-surface:     #13162B;
            --bg-user-bubble: #1C2045;
            --bg-ai-bubble:   #181B30;
            --accent:         #6B8BFF;
            --accent-glow:    rgba(107, 139, 255, 0.20);
            --accent-soft:    rgba(107, 139, 255, 0.10);
            --border:         rgba(107, 139, 255, 0.20);
            --text-primary:   #E8EAFF;
            --text-secondary: #8B90B8;
            --text-placeholder: #4A4F6E;
            --shadow-card:    0 2px 24px rgba(107,139,255,0.12), 0 1px 6px rgba(0,0,0,0.3);
        }
    }

    html, body, .stApp {
        background-color: var(--bg-base) !important;
        font-family: 'Sora', sans-serif !important;
        color: var(--text-primary) !important;
    }

    h1 {
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.9rem !important;
        background: linear-gradient(120deg, var(--accent) 0%, #A78BFA 60%, var(--accent) 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: shimmer 3.5s linear infinite;
        letter-spacing: -0.5px;
    }

    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    .stChatMessage {
        background-color: var(--bg-ai-bubble) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-bubble) !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: var(--shadow-card) !important;
        animation: bubbleIn 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) both;
        transition: box-shadow 0.2s ease;
        color: var(--text-primary) !important;
    }

    .stChatMessage:hover {
        box-shadow: var(--shadow-glow), var(--shadow-card) !important;
    }

    @keyframes bubbleIn {
        from { opacity: 0; transform: translateY(10px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    [data-testid="stChatMessageUser"] {
        background-color: var(--bg-user-bubble) !important;
        border-left: 3px solid var(--accent) !important;
    }

    [data-testid="stChatMessageAssistant"] {
        background-color: var(--bg-ai-bubble) !important;
        border-left: 3px solid #A78BFA !important;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stChatMessageAssistant"]::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(105deg, transparent 40%, var(--accent-soft) 50%, transparent 60%);
        background-size: 250% 100%;
        animation: scanline 4s linear infinite;
        pointer-events: none;
        border-radius: inherit;
    }

    @keyframes scanline {
        0%   { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        animation: pulse 2.8s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { filter: drop-shadow(0 0 3px var(--accent-glow)); }
        50%       { filter: drop-shadow(0 0 10px var(--accent)); }
    }

    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stMarkdown p {
        color: var(--text-primary) !important;
        line-height: 1.65 !important;
        font-size: 0.93rem !important;
    }

    [data-testid="stBottom"] {
        background: var(--bg-base) !important;
        border-top: 1px solid var(--border) !important;
        padding-top: 8px !important;
    }

    .stChatInput {
        background: var(--bg-surface) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-input) !important;
        box-shadow: 0 2px 12px var(--accent-glow) !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    .stChatInput:focus-within {
        border-color: var(--accent) !important;
        box-shadow: var(--shadow-glow) !important;
    }

    .stChatInput textarea {
        background: transparent !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.92rem !important;
        caret-color: var(--accent) !important;
    }

    .stChatInput textarea::placeholder {
        color: var(--text-placeholder) !important;
        font-style: italic;
    }

    .stChatInput button { color: var(--accent) !important; transition: filter 0.2s; }
    .stChatInput button:hover { filter: drop-shadow(0 0 6px var(--accent)) !important; }

    .stChatMessage code {
        background: var(--accent-soft) !important;
        color: var(--accent) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
        border-radius: 5px;
        padding: 2px 6px;
    }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--accent-glow); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
        font-family: 'Sora', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 PESCE Elite Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "✨"):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about PESCE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        try:
            if any(word in prompt.lower() for word in ["win", "winner", "contest", "prize"]):
                st.balloons()

            persona_prompt = f"You are the PESCE Elite Assistant for Mandya students. Answer professionally: {prompt}"

            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=persona_prompt
            )

            placeholder = st.empty()
            full_response = ""
            for word in response.text.split(" "):
                full_response += word + " "
                time.sleep(0.05)
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")

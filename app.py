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

    /* ── LIGHT MODE (default) ── */
    :root {
        --bg-base:          #F0F2FA;
        --bg-surface:       #FFFFFF;
        --bg-user-bubble:   #E8EEFF;
        --bg-ai-bubble:     #FFFFFF;
        --accent:           #4F6EF7;
        --accent-purple:    #A78BFA;
        --accent-glow:      rgba(79, 110, 247, 0.20);
        --accent-soft:      rgba(79, 110, 247, 0.07);
        --border:           rgba(79, 110, 247, 0.18);
        --text-primary:     #1A1D2E;
        --text-secondary:   #5A5E7A;
        --text-placeholder: #9CA3C0;
        --shadow-card:      0 2px 16px rgba(79,110,247,0.10), 0 1px 4px rgba(0,0,0,0.06);
        --shadow-glow:      0 0 0 3px rgba(79,110,247,0.18);
        --input-bg:         #FFFFFF;
        --input-border:     rgba(79, 110, 247, 0.35);
    }

    /* ── DARK MODE ── */
    [data-theme="dark"],
    [data-baseweb="base-provider"] [class*="st-emotion-cache"] {
        --bg-base:          #0D0F1A;
        --bg-surface:       #13162B;
        --bg-user-bubble:   #1C2045;
        --bg-ai-bubble:     #181B30;
        --accent:           #6B8BFF;
        --accent-purple:    #B39DFA;
        --accent-glow:      rgba(107, 139, 255, 0.22);
        --accent-soft:      rgba(107, 139, 255, 0.10);
        --border:           rgba(107, 139, 255, 0.22);
        --text-primary:     #E8EAFF;
        --text-secondary:   #8B90B8;
        --text-placeholder: #4A4F6E;
        --shadow-card:      0 2px 24px rgba(107,139,255,0.13), 0 1px 6px rgba(0,0,0,0.35);
        --shadow-glow:      0 0 0 3px rgba(107,139,255,0.22);
        --input-bg:         #13162B;
        --input-border:     rgba(107, 139, 255, 0.40);
    }

    /* ── BASE APP ── */
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        background-color: var(--bg-base) !important;
        font-family: 'Sora', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── FIX: bottom bar matches theme ── */
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    footer, .stChatFloatingInputContainer {
        background-color: var(--bg-base) !important;
        border-top: 1px solid var(--border) !important;
    }

    /* ── ANIMATED TITLE ── */
    h1 {
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.85rem !important;
        background: linear-gradient(120deg, var(--accent) 0%, var(--accent-purple) 55%, var(--accent) 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: shimmer 3.5s linear infinite;
        letter-spacing: -0.4px;
    }

    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* ── CHAT BUBBLES ── */
    .stChatMessage {
        background-color: var(--bg-ai-bubble) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: var(--shadow-card) !important;
        animation: bubbleIn 0.30s cubic-bezier(0.34, 1.56, 0.64, 1) both;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
        color: var(--text-primary) !important;
    }

    .stChatMessage:hover {
        box-shadow: var(--shadow-glow), var(--shadow-card) !important;
        transform: translateY(-1px);
    }

    @keyframes bubbleIn {
        from { opacity: 0; transform: translateY(12px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* User bubble */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, var(--bg-user-bubble) 0%, var(--bg-surface) 100%) !important;
        border-left: 3px solid var(--accent) !important;
    }

    /* AI bubble */
    [data-testid="stChatMessageAssistant"] {
        background: linear-gradient(135deg, var(--bg-ai-bubble) 0%, var(--bg-surface) 100%) !important;
        border-left: 3px solid var(--accent-purple) !important;
        position: relative;
        overflow: hidden;
    }

    /* Shimmer sweep on AI bubble */
    [data-testid="stChatMessageAssistant"]::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(105deg,
            transparent 38%, var(--accent-soft) 50%, transparent 62%);
        background-size: 280% 100%;
        animation: scanline 5s linear infinite;
        pointer-events: none;
        border-radius: inherit;
    }

    @keyframes scanline {
        0%   { background-position: 220% 0; }
        100% { background-position: -220% 0; }
    }

    /* Avatar glow */
    [data-testid="stChatMessageAvatarAssistant"] {
        animation: avatarPulse 3s ease-in-out infinite;
    }

    @keyframes avatarPulse {
        0%, 100% { filter: drop-shadow(0 0 2px var(--accent-glow)); }
        50%       { filter: drop-shadow(0 0 10px var(--accent)); }
    }

    /* Text inside bubbles */
    .stChatMessage p,
    .stChatMessage li,
    .stChatMessage span,
    .stMarkdown p {
        color: var(--text-primary) !important;
        line-height: 1.70 !important;
        font-size: 0.93rem !important;
    }

    /* ── INPUT BAR — full theme fix ── */
    div[data-testid="stChatInput"] {
        background-color: var(--input-bg) !important;
        border: 1.5px solid var(--input-border) !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 14px var(--accent-glow) !important;
        transition: border-color 0.25s, box-shadow 0.25s;
        overflow: hidden;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: var(--shadow-glow) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.92rem !important;
        caret-color: var(--accent) !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-placeholder) !important;
        font-style: italic;
    }

    div[data-testid="stChatInput"] button {
        color: var(--accent) !important;
        transition: filter 0.2s;
    }
    div[data-testid="stChatInput"] button:hover {
        filter: drop-shadow(0 0 7px var(--accent)) !important;
    }

    /* ── CODE BLOCKS ── */
    .stChatMessage code {
        background: var(--accent-soft) !important;
        color: var(--accent) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.81rem !important;
        border-radius: 5px;
        padding: 2px 6px;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ── ALERTS ── */
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
            
import streamlit as st
import os
import time

# Use this specific import style for Streamlit Cloud stability
try:
    from google import genai
except ImportError:
    import google.genai as genai

# Setup the Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Animated UI Polish
st.set_page_config(page_title="PESCE Elite Assistant", page_icon="✨")

st.markdown("""
    <style>
    /* 1. UNIVERSAL DARK THEME LOCK */
    .stApp {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }

    /* 2. FORCE TEXT VISIBILITY */
    h1, h2, h3, p, span, li, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* 3. FIX THE INPUT BAR (The "Shitty" Part) */
    /* Target the container */
    [data-testid="stChatInput"] {
        background-color: #1B2028 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    /* Target the actual text area */
    .stChatInput textarea {
        background-color: #262730 !important;
        color: white !important;
        caret-color: white !important;
    }

    /* Target the placeholder text (the "Ask about..." text) */
    .stChatInput textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        opacity: 1 !important;
    }

    /* 4. PREMIUM BUBBLES */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px);
        border-radius: 15px;
    }

    /* 5. ASSISTANT GLOW */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(66, 133, 244, 0.1) !important;
        border-left: 5px solid #4285F4 !important;
    }

    /* GRADIENT TITLE */
    h1 {
        background: linear-gradient(45deg, #4285F4, #34A853);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 PESCE Elite Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"]=="user" else "✨"):
        st.markdown(message["content"])

# 3. Handle Input with Typing Animation
if prompt := st.chat_input("Ask about PESCE..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Assistant Message
    with st.chat_message("assistant", avatar="✨"):
        try:
            # Check for winning keywords to trigger celebration
            if any(word in prompt.lower() for word in ["win", "winner", "contest", "prize"]):
                st.balloons()
            
            persona_prompt = f"You are the PESCE Elite Assistant for Mandya students. Answer professionally: {prompt}"
            
            response = client.models.generate_content(
                model='gemini-3.5-flash', 
                contents=persona_prompt
            )
            
            # THE TYPING ANIMATION (Match Winner Feature)
            placeholder = st.empty()
            full_response = ""
            for word in response.text.split(" "):
                full_response += word + " "
                time.sleep(0.05) # Speed of typing
                placeholder.markdown(full_response + "▌") # Cursor effect
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")
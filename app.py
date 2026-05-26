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
    /* 1. CASUAL LIGHT THEME */
    .stApp {
        background-color: #FFFFFF !important;
        color: #262730 !important;
    }

    /* 2. SOFT BLUE ACCENTS & READABLE TEXT */
    h1 {
        color: #4285F4 !important; /* Google Blue */
        font-weight: 700;
    }
    
    p, span, li, .stMarkdown {
        color: #3C4043 !important;
    }

    /* 3. CLEAN CHAT BUBBLES */
    .stChatMessage {
        background-color: #F1F3F4 !important; /* Light Grey */
        border: none !important;
        border-radius: 15px;
        margin-bottom: 10px;
        color: #3C4043 !important;
    }

    /* 4. ASSISTANT BUBBLE (Subtle Blue) */
    [data-testid="stChatMessageAssistant"] {
        background-color: #E8F0FE !important; /* Very Light Blue */
        border-left: 5px solid #4285F4 !important;
    }

    /* 5. THE INPUT BAR (Clean & Visible) */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border-top: 1px solid #DADCE0 !important;
    }

    .stChatInput textarea {
        background-color: #F1F3F4 !important;
        color: #202124 !important;
        border-radius: 10px !important;
    }

    /* Fix placeholder text for Light Mode */
    .stChatInput textarea::placeholder {
        color: #70757A !important;
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
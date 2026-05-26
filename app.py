import streamlit as st
import os
import time
# Use this exact import for the 2026 Google GenAI SDK
import google.genai as genai 

# 1. Setup the Client properly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Animated UI Polish
st.set_page_config(page_title="PESCE Elite Assistant", page_icon="✨")

# CSS for Animations
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Fade-in animation for chat bubbles */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage {
        animation: fadeIn 0.5s ease-out;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Soft pulse for Assistant messages */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(66, 133, 244, 0.05);
        border-left: 5px solid #4285F4;
        box-shadow: 0 0 15px rgba(66, 133, 244, 0.1);
    }

    h1 {
        background: linear-gradient(45deg, #4285F4, #34A853, #FBBC05, #EA4335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
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
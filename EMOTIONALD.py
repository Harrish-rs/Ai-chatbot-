import streamlit as st
import google.generativeai as genai
import os

class GeminiEmotionalChatbot:
    def __init__(self):
        # Configure with your API key
        api_key = "AIzaSyCzA9XuQqkWh4RuUv6ARmMH8fOgoCv7oZE"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []

    def get_response(self, user_input):
        try:
            prompt = f"""
            First, analyze the emotion in this message: "{user_input}"
            Then, respond empathetically in 1-2 sentences based on the detected emotion.
            Start your response with [EMOTION: detected_emotion] then provide your response.
            """
            
            response = self.chat.send_message(prompt)
            response_text = response.text
            
            if '[EMOTION:' in response_text:
                parts = response_text.split(']', 1)
                emotion = parts[0].split('[EMOTION:', 1)[1].strip()
                actual_response = parts[1].strip()
            else:
                emotion = 'neutral'
                actual_response = response_text
            
            return emotion, actual_response
            
        except Exception as e:
            st.error(f"Error: {e}")
            return "neutral", "I'm here to listen. Would you like to tell me more?"

def initialize_session_state():
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = GeminiEmotionalChatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(
        page_title="Emotional AI Chatbot",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("Emotional AI Chatbot")
    st.markdown("Chat with an AI that understands emotions 🤖💭")
    
    # Initialize session state
    initialize_session_state()
    
    # Chat interface
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Emotion Detected:** _{message['emotion']}_")
                st.markdown(f"**Assistant:** {message['content']}")
            st.markdown("---")
    
    # User input
    with st.container():
        user_input = st.text_input("Your message:", key="input", 
                                 placeholder="Type your message here...")
        if st.button("Send"):
            if user_input:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Get chatbot response
                emotion, response = st.session_state.chatbot.get_response(user_input)
                
                # Add bot response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "emotion": emotion
                })
                
                # Clear input and rerun
                st.rerun()

if __name__ == "__main__":
    main()
    
import streamlit as st
import google.generativeai as genai
import os

class GeminiEmotionalChatbot:
    def __init__(self, api_key):
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
            
            self.conversation_history.append({
                "user": user_input,
                "emotion": emotion,
                "bot": actual_response
            })
            
            return emotion, actual_response
            
        except Exception as e:
            st.error(f"Error: {e}")
            return "neutral", "I'm here to listen. Would you like to tell me more?"

def initialize_session_state():
    if 'chatbot' not in st.session_state:
        api_key = "YOUR_API_KEY"  # Replace with your API key
        st.session_state.chatbot = GeminiEmotionalChatbot(api_key)
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(page_title="AI Emotional Chatbot", page_icon="🤖")
    
    st.title("AI Emotional Chatbot 🤖")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f'You: {message["content"]}')
        else:
            with st.container():
                st.write(f'Emotion Detected: {message["emotion"]}')
                st.write(f'Chatbot: {message["content"]}')
    
    # Chat input
    user_input = st.text_input("Type your message here...", key="user_input")
    
    if st.button("Send", key="send"):
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get chatbot response
            emotion, response = st.session_state.chatbot.get_response(user_input)
            
            # Add bot response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "emotion": emotion
            })
            
            # Clear input
            st.session_state.user_input = ""
            
            # Rerun to update chat display
            st.rerun()

    # Add some styling
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)

    # Add a footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and Google's Gemini AI")

if __name__ == "__main__":
    main()

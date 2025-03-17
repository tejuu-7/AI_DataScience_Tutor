import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

# Configure Google AI
genai.configure(api_key=api_key)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.title("🤖 AI Data Science Tutor")
st.write("Ask any **data science-related** question!")

# Display chat history (latest messages first)
for chat in reversed(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(f"**You:** {chat['user']}")
    with st.chat_message("assistant"):
        st.markdown(f"**AI:** {chat['ai']}")

# User Input Box
user_input = st.chat_input("Type your data science question...")

if user_input:
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_input}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                # Step 1: AI Checks If the Question is Related to Data Science
                check_prompt = f"""
                You are an AI tutor for data science.
                - Check if the following question is **strictly** related to data science.
                - Answer with just **YES** or **NO** (no explanations).

                Question: "{user_input}"
                """
                check_response = llm.invoke(check_prompt).content.strip().lower()

                if check_response == "yes":
                    # Step 2: AI Answers the Question (Only if Related to Data Science)
                    response = llm.invoke(user_input).content

                    st.markdown(f"**AI:** {response}")

                    # Save chat history
                    st.session_state.chat_history.append({"user": user_input, "ai": response})
                else:
                    # Step 3: AI Rejects Non-Data Science Questions
                    st.markdown("**AI:** I can only answer data science-related questions. Please ask something related to data science. 😊")

                    # Save rejection response in chat history
                    st.session_state.chat_history.append({"user": user_input, "ai": "I can only answer data science-related questions. Please ask something related to data science. 😊"})

            except Exception as e:
                st.error(f"🚨 Error: {e}")
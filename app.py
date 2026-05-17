import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="MediAssist: Smart Healthcare Chatbot", 
    page_icon="🩺", 
    layout="centered"
)

# 2. Securely Initialize the Gemini Client
# Make sure your working API key is pasted inside these quotes!
API_KEY =  "AIzaSyAQ1lap3OJvQMHL_UuxL5skmjwibM7WIuk"
client = genai.Client(api_key=API_KEY)

# 3. System Prompt (Enforces a short, one-line disclaimer at the very end)
SYSTEM_PROMPT = (
    "You are 'MediAssist', an expert, highly empathetic, and polite digital healthcare guide. "
    "You speak clearly and use comforting, easy-to-understand terms.\n\n"
    "You must strictly follow these rules:\n"
    "1. Provide general educational information about symptoms and healthy lifestyle habits.\n"
    "2. Suggest common, easily accessible household solutions (like staying hydrated, warm water, or resting).\n"
    "3. NEVER give a final diagnosis or prescribe specific drug dosages.\n"
    "4. If the user mentions emergency symptoms (e.g., severe chest pain, sudden numbness, difficulty breathing), "
    "immediately alert them to call emergency medical services (like 911 or 102) right away and stop giving general advice.\n"
    "5. Always end your response with this exact one-line disclaimer: '*Disclaimer: Educational guidance only; always consult a real doctor for medical advice.*' Do not add any text after this."
)

# 4. Clean Header
st.title("🩺 MediAssist")
st.caption("✨ Smart Healthcare Chatbot Assistant")
st.write("---")

# 5. Initialize Chat History Tracker
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "👋 **Welcome! Hello there, friend.**\n\nI am **MediAssist**, your digital health guide. Your well-being is my priority! Whether you are dealing with a nagging headache, feeling under the weather, or just curious about healthy habits, feel free to tell me how you are feeling below.\n\n*How can I help make you feel more comfortable today?*"
        }
    ]

# 6. Render Active Chat History on Screen
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Interactive User Input Area
if user_prompt := st.chat_input("Tell MediAssist how you are feeling..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Restructure messages properly for the Gemini API
    formatted_contents = []
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    # 8. Get Safe AI Response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Analyzing symptoms carefully..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    )
                )
                bot_reply = response.text
                st.markdown(bot_reply)
                
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"An error occurred connecting to MediAssist: {e}")
import os
import pyperclip
import streamlit as st
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def model():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return ChatGoogleGenerativeAI(model="gemini-pro")

def getLLamaresponse(input_text,no_words,blog_style):
    ## Prompt Template
    template="""
        Write a {tone} blog in {lang} as {blog_style} for a topic {input_text} within {no_words} words with references and video links also if possible and ends with a conclusion. {info}
            """
    prompt=PromptTemplate(input_variables=['tone','lang',"blog_style","input_text",'no_words', "info"],
                          template=template)
    formated_prompt = prompt.format(tone=tone,lang=lang,blog_style=blog_style,input_text=input_text,no_words=no_words,info=info)
    ## Generate the ressponse from the LLama 2 model
    response=llm.invoke(formated_prompt)
    return response.content

def copy_text(answer, copy_button=False):
    pyperclip.copy(answer)
    if copy_button:
        st.toast("Text copied to clipboard!", icon="📋")

def record_audio():
    r = sr.Recognizer()
    with st.spinner("Recording..."):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            with st.spinner("Say Something..."):
                audio = r.listen(source, timeout=5)  # Set a timeout for listening
        with st.spinner("Processing..."):
            # Attempt speech recognition
            try:
                text = r.recognize_google(audio)
                st.session_state['input_text'] = text
                return text
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand what you said. Please try again or write in text box.")
                return ""
            except sr.RequestError as e:
                st.write(f"Could not request results; {e}")
                return ""

def input_state(input_text):
    if isinstance(input_text, str):
        st.session_state['input_text'] = input_text  # Update st.session_state with new text input



st.set_page_config(page_title="AI-Blogger",
                    page_icon='🤖',
                    layout='centered' )

st.header("AI Blogger 🤖", divider='rainbow')


col1,col2=st.columns([20,3])
with col1:
    st.write('')
    text = st.empty()
    input_text = text.text_input("Enter the Blog Topic")
    

with col2:
    st.write(':grey[.]')
    recorder = st.button("🎙️", help="Blog Topic by Voice")

if recorder:
    recorded_text = record_audio()
    if recorded_text:
        input_text = text.text_input("Enter the Blog Topic",value=recorded_text)

with st.sidebar:
    st.title(' :blue[_AI Generated Blog_] 🤖')
    # Refactored from <https://github.com/a16z-infra/llama2-chatbot>
    st.subheader('Parameters')
    no_words = st.sidebar.slider('Maximum Characters', min_value=10, max_value=5000, value=1000, step=100)
    blog_style=st.selectbox('Writing the blog for', ('Researchers','Data Scientist','Common People'),index=0)
    tone=st.selectbox('Desired Tone', ('Informative','Casual','Persuasive', 'Formal', 'Humorous'),index=0)
    lang = st.text_input('Language', 'English')
    info = st.text_input('Specific Instruction')
    with st.spinner("Loading Model..."):
        llm= model()

submit=st.button("Generate Blog", on_click =lambda: input_state(input_text))
if submit:
    with st.spinner("Generating Blog..."):
        answer = getLLamaresponse(st.session_state['input_text'],no_words,blog_style)
        st.success('Blog Generated!', icon="✅")
        st.write(answer)
        st.markdown(''':orange[Run in your system to access Copy to Clipboard Feature]''')

        ## Uncomment if using in system HF doesn't Support Copy to clipboard
        # st.button("📋", on_click=copy_text(answer))

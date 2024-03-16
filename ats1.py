import os
import pyperclip
import streamlit as st
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class ATS(object):
    def __init__(self, title="ATS Tracking System"):
        self.title = title

    @staticmethod
    def model():
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        return ChatGoogleGenerativeAI(model="gemini-pro")

    @staticmethod
    def get_gemini_response(llm, input_text, doc, template, info=''):
        formated_prompt = template.format(doc=doc, input_text=input_text)
        response = llm.invoke(formated_prompt)
        return response.content
        # return formated_prompt

    @staticmethod
    def copy_text(answer, copy_button=False):
        pyperclip.copy(answer)
        if copy_button:
            st.toast("Text copied to clipboard!", icon="📋")

    @staticmethod
    def record_audio():
        r = sr.Recognizer()
        with st.spinner("Recording..."):
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                with st.spinner("Say Something..."):
                    audio = r.listen(source, timeout=5)
            with st.spinner("Processing..."):
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

    @staticmethod
    def input_state(input_text):
        if isinstance(input_text, str):
            st.session_state['input_text'] = input_text


def run_ats(doc=''):
    load_dotenv()
    ats = ATS()
    st.header(ats.title + " 🤖", divider='rainbow')
    input_text=st.text_area("Job Description: ",key="input")
    # uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


    # if uploaded_file is not None:
        # st.write("PDF Uploaded Successfully")
        

    with st.sidebar:
        st.title(' :blue[_AI Generated ATS] 🤖')
        st.subheader('Parameters')
        
        with st.spinner("Loading Model..."):
            llm = ats.model()
    submit1 = st.button("Tell Me About the Resume")

    # submit2 = st.button("How Can I Improvise my Skills")

    submit3 = st.button("Percentage match")

    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

    Job Description: {input_text}
    Resume: {doc}
    """

    input_prompt3 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.

    Job Description: {input_text}
    Resume: {doc}
    """

    if submit1:
        if doc is not None:
            response=ats.get_gemini_response(llm=llm,template=input_prompt1,doc=doc,input_text=input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

    elif submit3:
        if doc is not None:
            response=ats.get_gemini_response(llm=llm,template=input_prompt3,doc=doc,input_text=input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume")

if __name__ == "__main__":
    run_ats()
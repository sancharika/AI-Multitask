import streamlit as st
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import pyperclip
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GOOGLE_API_KEY']='AIzaSyAA59xkxMEUqffuaNMzrTxK6m5AJpY3tCw'

def model():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return ChatGoogleGenerativeAI(model="gemini-pro")

def getLLamaresponse(input_text,no_words,blog_style):
    
    ## Prompt Template

    template="""
        Write a {tone} blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words and ends with a conclusion. {info}.
            """
    
    prompt=PromptTemplate(input_variables=['tone',"blog_style","input_text",'no_words', "info"],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm.invoke(prompt.format(tone=tone,blog_style=blog_style,input_text=input_text,no_words=no_words,info=info))
    print(response)
    return response.content

def copy_text(answer, copy_button=False):
    pyperclip.copy(answer)
    if copy_button:
        st.toast("Text copied to clipboard!", icon="📋")


st.set_page_config(page_title="AI-Blogger",
                    page_icon='🤖',
                    layout='centered' )

st.header("AI Blogger 🤖", divider='rainbow')


input_text=st.text_input("Enter the Blog Topic")

with st.sidebar:
    st.title(' :blue[_AI Generated Blog_] 🤖')

    # Refactored from <https://github.com/a16z-infra/llama2-chatbot>
    st.subheader('Parameters')
    
    no_words = st.sidebar.slider('Maximum Characters', min_value=10, max_value=5000, value=1000, step=100)
    blog_style=st.selectbox('Writing the blog for',
                            ('Researchers','Data Scientist','Common People'),index=0)
    tone=st.selectbox('Desired Tone',
                            ('Informative','Casual','Persuasive', 'Formal', 'Humorous'),index=0)

    info = st.text_input('Specific Instruction')
    with st.spinner("Loading Model..."):
        llm= model()
        
    
submit=st.button("Generate Blog")


## Final response
if submit:
    with st.spinner("Generating Blog..."):
        answer = getLLamaresponse(input_text,no_words,blog_style)
        st.success('Blog Generated!', icon="✅")
        st.write(answer)

        ## Uncomment if using in system HF doesn't Support Copy to clipboard
        # st.button("📋", on_click=copy_text(answer))
        st.markdown('''


                :orange[Run in your system to access Copy to Clipboard Feature]
        ''')

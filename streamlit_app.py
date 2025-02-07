import streamlit as st

import os


from openai import OpenAI
from anthropic import Anthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic



def text_generator(input_text: str, systemprompt_text: str) -> str:
    """
    Generate a cover letter using Claude, given a resume and job description.
    
    Args:
        input_text (str): The text content of the input file
            
    Returns:
        str: The generated text
    """
    # Initialize the Claude client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Create the model using LangChain
    model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", systemprompt_text),
        ("user", """
        Input:
        {input}
        
        Instructions:
        {instructions}
        
        Please write a cover letter based on the above information.
        """)
    ])
    
    # Create the chain
    chain = prompt | model | StrOutputParser()
    
    # Generate the cover letter
    result_text = chain.invoke({
        "input": input_text,
        "instructions": instructions_text
    })
    
    return result_text


st.text_area("Instructions", height=100)

t_result, t_input, t_systemprompt  = st.tabs(["Result","Input", "SystemPrompt" ])


with st.sidebar:
    st.title("Code Assistant")
    st.write("Python coding assistant.")

    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    anthropic_api_key = st.text_input("Anthropic API Key", key="anthropic_api_key", type="password")
    "[Get an Anthropic API key](https://console.anthropic.com/settings/keys)"
    
    
    input_file = st.file_uploader("Upload your input text file (txt)", type="txt")
    systemprompt_file = st.file_uploader("Upload the system prompt (txt)", type="txt")

with t_input:
    st.subheader("Input")
    st.text_area("Input Text", height=600)

if systemprompt_file:   
    systemprompt_text = systemprompt_file.read().decode("utf-8")
    with t_systemprompt:
        st.subheader("System Prompt")
        #md = st.text_area("System Prompt Text", systemprompt_text, height=100, label_visibility='hidden')
        st.write(f"Length: {len(systemprompt_text)} characters.")
        st.markdown(systemprompt_text)
        

if input_file:
    input_text = input_file.read().decode("utf-8")

    with t_input:
        st.text_area("Input Text", input_text, height=600)

    with st.sidebar:
        generate_button = st.button("Generate")


    if generate_button:

        result = text_generator(input_text,systemprompt_text)
      
        with t_result:
            st.subheader("Result")
            st.text_area("Result Text", result, height=600)
        
        with st.sidebar:
            st.success("Result Generated")
# Importing libraries
import streamlit as st
from streamlit_chat import message
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

# Initialize the API key
openai_api_key = "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"

# Set page title
st.set_page_config(page_title="CSV Reader")

# Create a sidebar to display information
with st.sidebar:
   st.header("Datahut")
   st.markdown("""
   ## About
   This is a chatbot designed by Datahut to interact with a csv file and extract information from it.
   Simplify your data analysis process with our user-friendly chatbot which enables you to quickly retrieve key information from your CSV files.
   """)

st.header("CSV Reader ")
# File uploader function
user_csv = st.file_uploader("Upload your CSV file", type="csv")
if user_csv is not None:
   # Get the user input
   user_input = get_text()
   # Initialize the OpenAI model
   llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key=openai_api_key, temperature=0)
   # Initialize the agent
   agent = create_csv_agent(llm, user_csv, verbose=True)
   # Initialize the session state
   if 'generated' not in st.session_state:
       st.session_state['generated'] = ["Yes, you can!"]
   if 'past' not in st.session_state:
       st.session_state['past'] = ["Can I ask anything about my csv file?"]
   if user_input:
       st.session_state.past.append(user_input)
       # Get the chatbot response
       response = get_response(user_input)
       st.session_state.generated.append(response)
   # Displaying the chat
   if len(st.session_state['generated']) != 1:
       for i in range(1,len(st.session_state['generated'])):
           message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
           message(st.session_state['generated'][i], key=str(i))

# Function to get user input
def get_text():
   input_text = st.text_input("Enter your question")
   return input_text

# Function to generate response to user question
def get_response(query):
   with st.spinner(text="In progress"):
       response = agent.run(query)
   return response

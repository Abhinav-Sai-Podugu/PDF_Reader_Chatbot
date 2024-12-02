from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import api_key
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings.bedrock import BedrockEmbeddings
import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv

load_dotenv()
# x = os.getenv("OPENAI_API_KEY")

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer


def pdf_text(pdfs):
    text = ""
    for p in pdfs:
        reader = PdfReader(p)
        for page in reader.pages:
            text += page.extract_text()
    return text

def chunks(text):
    splitter = CharacterTextSplitter(separator = "\n", chunk_size = 1000, chunk_overlap = 200, length_function = len)
    chunk = splitter.split_text(text)
    return chunk


# def embeddings(chunks):
#     model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     embd = CustomSentenceTransformerEmbeddings(model_name)
#     vectors = FAISS.from_texts(texts=chunks, embedding=embd)
#     return vectors


def embeddings(chunks):
    # model1 = OpenAIEmbeddings(api_key = x)
    # model2 = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    # name = "sentence-transformers/all-MiniLM-L6-v2"
    # model3 = HuggingFaceEmbeddings(model_name = name)
    # vectors = FAISS.from_texts(texts = chunks, embedding = model3)
    # return vectors

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("fiass_index")


def chain(embed):
    # llm = ChatOpenAI()
    #  llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
    prompt_template = """
            Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
            provided context just say, "Sorry, I didn’t understand your question. Do you want to connect with a live agent?", don't provide the wrong answer\n\n
            Context:\n {context}?\n
            Question: \n{question}\n

            Answer:
            """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def userinput(input):
    response = st.session_state.conversation({'question': input})
    st.write(response)
    st.session_state.chat_history = response['chat_history']

    for i, msg in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            message(msg.content, is_user = True, key = str(i) + '_user')
        else:
            message(msg.content, is_user = False, key = str(i) + '_ai')
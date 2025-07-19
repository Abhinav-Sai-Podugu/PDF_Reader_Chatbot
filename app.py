from PyPDF2 import PdfReader
import streamlit as st
from streamlit_chat import message

from langchain.retrievers import MultiQueryRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()
import os

os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_API_BASE"]


def pdf_text(pdfs):
    text = ""
    for p in pdfs:
        try:
            reader = PdfReader(p)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    st.warning(f"Could not extract text from page {reader.pages.index(page)}.")
        except Exception as e:
            st.error(f"Error processing file {p.name}: {e}")
    return text


def chunks(text):
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = splitter.split_text(text)
    doc = [Document(page_content=chunk, metadata={"source": "PDF"}) for chunk in chunks]
    return doc


def embeddings(chunks):
    try:
        st.info("Creating embeddings...")
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        vector = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name="openrouter-rag",
            persist_directory="./chroma_data"
        )
        vector.persist()
        st.success("Embeddings created successfully!")
        return vector
    except Exception as e:
        st.error(f"Failed to create embeddings: {e}")
        return None


def chain(embed):
    llm = ChatOpenAI(model="mistralai/mistral-7b-instruct", temperature=0.2)

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate 2
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )
    retriever = MultiQueryRetriever.from_llm(embed.as_retriever(), llm, prompt=QUERY_PROMPT)

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}

    If the answer is not in the provided context, respond with: "Sorry, I didn’t understand your question. Do you want to connect with a live agent?"
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    return chain


def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon=":books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "new_message" not in st.session_state:
        st.session_state.new_message = ""

    st.markdown("""
    <style>
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            position: fixed !important;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: white;
            padding: 1rem;
            border-bottom: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)

    static_container = st.container()

    with static_container:
        st.header("Chat with PDFs :books:")
        input_text = st.text_input("Ask a question about your documents:")

    st.markdown('<div style="padding-top: 5rem; "></div>', unsafe_allow_html=True)

    if input_text and st.session_state.get("conversation"):
        try:
            response = st.session_state.conversation.invoke({'question': input_text})
            st.session_state.chat_history.append({"user": input_text, "bot": response})
            for i, msg in enumerate(st.session_state.chat_history):
                message(msg["user"], is_user=True, key=f"user_{i}")
                message(msg["bot"], is_user=False, key=f"bot_{i}")
        except Exception as e:
            st.error(f"Error during conversation: {e}")

    with st.sidebar:
        st.subheader("Your Documents")
        pdfs = st.file_uploader("Upload your documents in PDF format", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                try:
                    text = pdf_text(pdfs)
                    if text:
                        chunk = chunks(text)
                        vector = embeddings(chunk)
                        if vector:
                            st.session_state.conversation = chain(vector)
                            st.success("Documents processed successfully!")
                        else:
                            st.error("Failed to process embeddings.")
                    else:
                        st.error("No text extracted from the uploaded documents.")
                except Exception as e:
                    st.error(f"Error processing documents: {e}")


if __name__ == '__main__':
    main()
from Main import pdf_text, chunks, embeddings, chain, userinput
from htmlTemplates import css, bot_template, user_template
import streamlit as st
from streamlit import sidebar
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    st.set_page_config(page_title = "Chat with PDFs", page_icon = ":books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.write(css, unsafe_allow_html=True)


    st.header("Chat with PDFs :books:")
    input = st.text_input("Ask a question about your documents:")

    if input:
        userinput(input)

    st.write(user_template.replace("{{MSG}}", "Hello Human"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello ROBOT"), unsafe_allow_html=True)


    with st.sidebar:
        st.subheader("Your Documents")
        pdfs = st.file_uploader("Upload your documents in PDF format", accept_multiple_files = True)
        if st.button("Process"):
            with st.spinner("Processing"):
                text = pdf_text(pdfs)
                chunk = chunks(text)
                vector = embeddings(chunk)
                st.session_state.conversation = chain(vector)

                st.success("Done")



if __name__ == '__main__':
    main()
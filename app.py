import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from htmlTemplates import css, bot_template, user_template, info_template
from langchain.prompts import PromptTemplate
from answer_length import get_max_tokens, check_answer_length_change, update_processed_answer_length

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)   
            for page in pdf_reader.pages:
                text = text + page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    
    return text  # we will get single string of raw text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=300,
        length_function = len
    )
    chunks = text_splitter.split_text(text)

    return chunks

def get_vectorstore(chunks):
    #embeddings = OpenAIEmbeddings()
    try:
        embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        return vectorstore
    
    except Exception as e:
        st.error(f"Failed to generate embeddings or vectore store: {e}")
        return None

def get_conversation_chain(vectorstore,length_type):
    llm = ChatOpenAI(
        model='llama3-8b-8192',
        base_url="https://api.groq.com/openai/v1",
        temperature=0.6,
        max_tokens=get_max_tokens(length_type),
        openai_api_key=os.getenv("GROQ_API_KEY")
    )
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

    # Prompt to make the retriever history-aware
    history_aware_prompt = PromptTemplate.from_template(
        """
        Given the following conversation and a follow up question, rephrase the follow up question 
        to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {input}
        Standalone question:
        """
    )

    # Create history-aware retriever with prompt
    retriever = create_history_aware_retriever(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        prompt=history_aware_prompt
    )

    # Final prompt for the LLM to respond
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the following context to answer the question: {context}"),
        ("human", "{input}")
    ])

    # Create document chain
    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=final_prompt
    )

    # Create final retrieval chain
    conversation_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain
    )

    return conversation_chain

def handle_user_input(user_question):
    try:
        if st.session_state.conversation is None:
            # No PDFs processed yet
            st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", "Oops! I’m all ears, but I need those PDFs first, feed me some docs!"), unsafe_allow_html=True)
            return

        response = st.session_state.conversation.invoke({'input': user_question})
        bot_answer = response['answer']

        # Store this turn in session history
        if "chat_log" not in st.session_state:
            st.session_state.chat_log = []
        
        st.session_state.chat_log.append(("user", user_question))
        st.session_state.chat_log.append(("bot", bot_answer))

        # Display the full chat
        MAX_VISIBLE_CHARS = 400  # You can adjust this threshold

        for sender, msg in st.session_state.chat_log:
            if sender == "user":
                st.write(user_template.replace("{{MSG}}", msg), unsafe_allow_html=True)
            else:
                if len(msg) > MAX_VISIBLE_CHARS:
                    with st.expander("Show full answer"):
                        st.write(bot_template.replace("{{MSG}}", msg), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", msg), unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Bot ran into a hiccup: {e}")

def main():
    try:
        load_dotenv()

        st.set_page_config(page_title="Gyaantra Docs", page_icon=":books:")

        st.write(css, unsafe_allow_html=True)
        # initialize session state before -- good practice
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        
        if "chat_log" not in st.session_state:
            st.session_state.chat_log = []

        # Track the processed answer length
        if "processed_answer_length" not in st.session_state:
            st.session_state.processed_answer_length = None

        st.header("Gyaantra Docs :books:")
        user_questions = st.text_input("Ask Questions about yout documents")

        if user_questions:
            handle_user_input(user_questions)

        with st.sidebar:
            st.header("Chat with multiple PDFs")
            st.markdown(info_template, unsafe_allow_html=True)
            pdf_docs = st.file_uploader("Upload your PDFs here and click on process", accept_multiple_files=True)

            answer_length = st.sidebar.selectbox(
                "Answer Length",
                options=["Short", "Medium", "Long"],
                index=1  # default to medium
            )
            
            # Check and display message based on answer length change
            check_answer_length_change(answer_length)


            if st.button("Process"):

                with st.spinner("Processing"):
                    # get the pdf text 
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store with embeddings
                    vector_store = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store, answer_length)

                    update_processed_answer_length(answer_length)

                    st.success("Processed successfully")

            if st.button("Clear Chat"):
                st.session_state.chat_log = []
                st.success("Chat cleared!")

    except Exception as e:
        st.error(f" Unexpected error: {e}")


if __name__=='__main__':
    main()
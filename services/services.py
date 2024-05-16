import random
# from openai import OpenAI
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from services.prompts import main_prompt
from dotenv import load_dotenv
import os

load_dotenv()
MISTRALAI_API_KEY = os.getenv("MISTRALAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def random_response():
    return random.choice(["Oui", "Non"])


def load_document(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    return documents


def RAG_mistralAI(message, history):
    documents = load_document("data/AJ_chemicals.pdf")

    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=MISTRALAI_API_KEY)
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()

    model = ChatMistralAI(
        model="open-mistral-7b",
        mistral_api_key=MISTRALAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(main_prompt)

    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": message, "context": history})
    return response


# def RAG_openAI(message, history):
#     documents = load_document("data/AJ_chemicals.pdf")

#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#     vector = FAISS.from_documents(documents, embeddings)
#     retriever = vector.as_retriever()

#     model = OpenAI(
#         model_name="gpt-3.5-turbo",
#         openai_api_key=OPENAI_API_KEY)
#     prompt = ChatPromptTemplate.from_template(main_prompt)

#     document_chain = create_stuff_documents_chain(model, prompt)
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)

#     response = retrieval_chain.invoke({"input": message, "context": history})
#     return response["answer"]

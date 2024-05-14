import random
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from prompts import main_prompt
from dotenv import load_dotenv
import os

load_dotenv()
MISTRALAI_API_KEY = os.getenv("MISTRALAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def random_response():
    return random.choice(["Oui", "Non"])


def RAG_mistralAI(message, history):

    loader = PyPDFLoader("data/AJ_chemicals.pdf")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=MISTRALAI_API_KEY)
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()

    model = ChatMistralAI(model="open-mistral-7b", mistral_api_key=MISTRALAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(main_prompt)

    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": message, "context": history})
    return response["answer"]

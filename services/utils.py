
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
MISTRALAI_API_KEY = os.getenv("MISTRALAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def load_document(file_path):
    """Charge un document du format PDF"""
    loader = PyPDFLoader(file_path)
    document = loader.load()
    return document


def split_document(document):
    """Découpe un document en plusieurs parties"""
    text_splitter = RecursiveCharacterTextSplitter()
    splitted_document = text_splitter.split_documents(document)
    return splitted_document


def embed_document(splitted_document):
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=MISTRALAI_API_KEY)
    embeded_document = FAISS.from_documents(splitted_document, embeddings)
    return embeded_document

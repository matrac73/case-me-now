
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import re

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


def split_document_by_sections(text):
    pattern_IP = r"Private copy of .*?Copy and Sharing Prohibited."
    cleaned_text = re.sub(pattern_IP, '', text, flags=re.S)
    pattern = re.compile(r'\d+/\d+$')
    lines = cleaned_text.split('\n')
    filtered_lines = [line for line in lines if not pattern.search(line.strip())]
    filtered_text = '\n'.join(filtered_lines)

    case_sections_dict = {}

    Problem_definition_search = re.search(r"Problem definition(.*?)Question 1", filtered_text, re.S)
    if Problem_definition_search:
        Problem_definition = Problem_definition_search.group(1).strip()
        case_sections_dict['Problem_definition'] = Problem_definition

    suite = True
    i = 0

    while suite:
        i += 1
        question_search = re.search(rf"Question {i}(.*?)Possible answer", filtered_text, re.S)
        if question_search:
            question = question_search.group(1).strip()
            case_sections_dict[f'Question_{i}'] = question
            filtered_text = re.sub(rf"Question {i}(.*?)Possible answer", "Possible answer", filtered_text, 1, re.S)
        else:
            suite = False
            break

        answer_search = re.search(rf"Possible answer(.*?)Question {i+1}", filtered_text, re.S)
        if answer_search:
            answer = answer_search.group(1).strip()
            case_sections_dict[f'Answer_{i}'] = answer
            filtered_text = re.sub(rf"Possible answer(.*?)Question {i+1}", rf"Question {i+1}", filtered_text, 1, re.S)
        else:
            answer_search = re.search(r"Possible answer(.*)", filtered_text, re.S)
            answer = answer_search.group(1).strip()
            case_sections_dict[f'Answer_{i}'] = answer
            filtered_text = re.sub(r"Possible answer(.*)", "", filtered_text, 1, re.S)

    return case_sections_dict

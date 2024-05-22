
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


def embed_document(splitted_document):
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=MISTRALAI_API_KEY)
    embeded_document = FAISS.from_documents(splitted_document, embeddings)
    return embeded_document


def split_document(document):
    """Découpe un document en plusieurs parties"""
    text_splitter = RecursiveCharacterTextSplitter()
    splitted_document = text_splitter.split_documents(document)
    return splitted_document


def split_document_by_sections(document):
    text = ""
    for i in range(len(document)):
        text += document[i].page_content + " "

    pattern_IP = r"Private copy of .*?Copy and Sharing Prohibited."
    cleaned_text = re.sub(pattern_IP, '', text, flags=re.S)
    pattern = re.compile(r"^\s*(\[[^\]]+\]|[A-Za-z ]+)\s*-\s*\d+/\d+\s*$")
    lines = cleaned_text.split('\n')
    filtered_lines = [line for line in lines if not pattern.search(line.strip())]
    filtered_lines = [line for line in filtered_lines if line != ' ' and line != '  ' and line != '   ']
    filtered_text = '\n'.join(filtered_lines)

    case_sections_dict = {}

    Intro_search = re.search(r"(.*?)Problem definition", filtered_text, re.S)
    if Intro_search:
        Intro = Intro_search.group(1).strip()
        case_sections_dict['Intro'] = Intro
        filtered_text = re.sub(r"(.*?)Problem definition", "Problem definition", filtered_text, 1, re.S)

    Problem_definition_search = re.search(r"Problem definition(.*?)Question +1", filtered_text, re.S)
    if Problem_definition_search:
        Problem_definition = Problem_definition_search.group(1).strip()
        case_sections_dict['Problem_definition'] = Problem_definition
        filtered_text = re.sub(r"Problem definition(.*?)Question +1", "Question 1", filtered_text, 1, re.S)

    for i in range(1, 10):
        question_search = re.search(rf"Question +{i}(.*?)Possible answer", filtered_text, re.S)
        if question_search:
            question = question_search.group(1).strip()
            case_sections_dict[f'Question_{i}'] = question
            filtered_text = re.sub(rf"Question +{i}.*?Possible answer", "Possible answer", filtered_text, 1, re.S)
        else:
            continue

        answer_search = re.search(rf"Possible answer(.*?)Question +{i+1}", filtered_text, re.S)
        answer_search_skip = re.search(rf"Possible answer(.*?)Question +{i+2}", filtered_text, re.S)
        if answer_search:
            answer = answer_search.group(1).strip()
            case_sections_dict[f'Answer_{i}'] = answer
            filtered_text = re.sub(rf"Possible answer(.*?)Question +{i+1}", rf"Question {i+1}", filtered_text, 1, re.S)
        elif answer_search_skip:
            answer = answer_search_skip.group(1).strip()
            case_sections_dict[f'Answer_{i}'] = answer
            filtered_text = re.sub(rf"Possible answer(.*?)Question +{i+2}", rf"Question {i+2}", filtered_text, 1, re.S)
        else:
            answer_search = re.search(r"Possible answer(.*)", filtered_text, re.S)
            answer = answer_search.group(1).strip()
            case_sections_dict[f'Answer_{i}'] = answer
            filtered_text = re.sub(r"Possible answer(.*)", "", filtered_text, 1, re.S)

    return case_sections_dict

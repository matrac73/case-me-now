import gradio as gr
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from services.prompts import main_prompt
from services.utils import load_document, split_document, embed_document
from dotenv import load_dotenv
import time as t
import os

load_dotenv()
MISTRALAI_API_KEY = os.getenv("MISTRALAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def init_RAG():
    document = load_document("data/AJ_chemicals.pdf")
    splitted_document = split_document(document)
    embeded_document = embed_document(splitted_document)

    LLM_model = ChatMistralAI(model="open-mistral-7b", mistral_api_key=MISTRALAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(main_prompt)

    document_chain = create_stuff_documents_chain(LLM_model, prompt)
    retriever = embeded_document.as_retriever()

    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain


retrieval_chain = init_RAG()


def inference_RAG(message, history, retrieval_chain):
    response = retrieval_chain.invoke({"input": message, "context": history})
    return response


def history_generator(history):
    response = inference_RAG(history[0][0], history[0][1], retrieval_chain)['answer']
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        t.sleep(0.01)
        yield history


def add_message(history, message):
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)


# def transcript(audio):
#     try:
#         client = OpenAI(api_key=OPENAI_API_KEY)
#         audio_file = open(audio, "rb")
#         transcriptions = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=audio_file,
#             response_format="text"
#         )
#         return transcriptions
#     except Exception as error:
#         print(str(error))
#         raise gr.Error("An error occurred while generating speech. Please check your API key and try again.")

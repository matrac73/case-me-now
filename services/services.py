import os
from dotenv import load_dotenv
import time as t
import gradio as gr
from pathlib import Path

from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from services.prompts import system_prompt, intro_prompt, question_answers_prompts

load_dotenv()
MISTRALAI_API_KEY = os.getenv("MISTRALAI_API_KEY")
client = OpenAI()


def inference(history, user_prompt):
    client = MistralClient(api_key=MISTRALAI_API_KEY)
    history_chatMessage = [ChatMessage(role="system", content=system_prompt)]
    for i in range(len(history)-2):
        history_chatMessage.append(ChatMessage(role="user", content=history[i+1][0]))
        history_chatMessage.append(ChatMessage(role="assistant", content=history[i+1][1]))
    history_chatMessage.append(ChatMessage(role="user", content=user_prompt))

    chat_response = client.chat(model="open-mistral-7b", messages=history_chatMessage)
    answer = chat_response.choices[0].message.content
    return answer


def history_generator(history):
    response = inference(history, history[-1][0])
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        t.sleep(0.01)
        yield history


def submit_message(history, message):
    if 'files' in message:
        for x in message["files"]:
            history.append([x, None])
    if 'text' in message:
        history.append([message["text"], None])
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def handle_audio(audio_path):
    text = STT(audio_path)
    if text:
        return text
    return "Désolé, je n'ai pas pu reconnaître l'audio."


def submit_audio(history, audio_file):
    text = handle_audio(audio_file)
    message = {'text': text, 'files': []}
    return submit_message(history, message)


def STT(audio_file_path):
    audio_path = Path(audio_file_path)
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_path,
        response_format="text"
        )
    return transcription


def generate_speech(history):
    text = history[-1][-1]
    speech_file_path = Path("data/generated_speech.mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

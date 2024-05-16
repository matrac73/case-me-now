import gradio as gr
import time
from services.services import RAG_mistralAI


def add_message(history, message):
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def bot(history):
    response = RAG_mistralAI(history[0][0], history[0][1])['answer']
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.02)
        yield history


with gr.Blocks(css="footer{display:none !important}", fill_height=True) as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        show_copy_button=True
    )

    chat_input = gr.MultimodalTextbox(
        interactive=True,
        file_types=["image"],
        placeholder="Enter message or upload file...",
        show_label=False
        )

    chat_msg = chat_input.submit(
        fn=add_message,
        inputs=[chatbot, chat_input],
        outputs=[chatbot, chat_input]
        )

    bot_msg = chat_msg.then(bot, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

demo.queue()
if __name__ == "__main__":
    demo.launch(favicon_path="./data/favicon.ico")

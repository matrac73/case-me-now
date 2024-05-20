import gradio as gr
from services.services import submit_message, history_generator, submit_audio

css = """
html, body, #root {
    height: 100%;
}
footer {
    display: none !important;
}
"""


with gr.Blocks(css=css, fill_height=True) as demo:

    chatbot = gr.Chatbot(
        value=[],
        elem_id="chatbot",
        bubble_full_width=False,
        show_copy_button=True
    )

    chat_input = gr.MultimodalTextbox(
        interactive=True,
        file_types=['image'],
        placeholder="",
        show_label=False
    )

    audio_listener = gr.Audio(
        sources=["microphone"],
        type="filepath"
    )

    send_audio_btn = gr.Button("Envoyer Audio")

    chatbot.height = '82vh'

    chat_msg = chat_input.submit(
        fn=submit_message,
        inputs=[chatbot, chat_input],
        outputs=[chatbot, chat_input]
    )

    bot_msg = chat_msg.then(history_generator, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

    audio_msg = send_audio_btn.click(
        fn=submit_audio,
        inputs=[chatbot, audio_listener],
        outputs=[chatbot, chat_input]
    )

    bot_msg = audio_msg.then(history_generator, chatbot, chatbot, api_name="bot_response")
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

demo.queue()
if __name__ == "__main__":
    demo.launch(favicon_path="./data/favicon.ico")

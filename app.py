import gradio as gr
from services.services import submit_message, history_generator, submit_audio, generate_speech
from services.theme import theme

css = """
html, body, #root {
    height: 100%;
}
footer {
    display: none !important;
}
"""

with gr.Blocks(css=css, fill_height=True, theme=theme) as demo:
    with gr.Tab("Copilot"):
        with gr.Column():
            chatbot = gr.Chatbot(
                value=[],
                label="Conversation",
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

            chat_msg = chat_input.submit(
                fn=submit_message,
                inputs=[chatbot, chat_input],
                outputs=[chatbot, chat_input]
            )

            bot_msg = chat_msg.then(history_generator, chatbot, chatbot, api_name="bot_response")
            bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

            with gr.Row():
                audio_listener = gr.Audio(
                    sources=["microphone"],
                    label="Entrée Audio",
                    type="filepath"
                )

                send_audio_btn = gr.Button("Envoyer Audio")
                listen_btn = gr.Button("Écouter la réponse")

                audio_msg = send_audio_btn.click(
                    fn=submit_audio,
                    inputs=[chatbot, audio_listener],
                    outputs=[chatbot, chat_input]
                )

                audio_response = audio_msg.then(history_generator, chatbot, chatbot, api_name="bot_response")
                audio_response.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

                listen_msg = listen_btn.click(
                    fn=generate_speech,
                    inputs=[chatbot],
                    outputs=gr.Audio(
                        label="Sortie Audio",
                        type="filepath"
                    )
                )

    with gr.Tab("Case générator"):
        with gr.Column():

            language = gr.Radio(
                choices=["Anglais", "Français", "Italien", "Espagnol"],
                label="Langue",
                value="Français"
            )

            difficulty = gr.Slider(
                minimum=1,
                maximum=3,
                step=1,
                label="Difficulté du cas",
                value=2
            )

            case_type = gr.Radio(
                choices=["Interviewer-led", "Candidate-led", "Estimation case", "Written case"],
                label="Type de cas",
                value="Interviewer-led"
            )

            case_functions = gr.CheckboxGroup(
                choices=["Réduction des coûts", "Science des données", "Digital", "Marketing digital", "Stratégie de croissance"],
                label="Fonctions du cas",
                value=["Digital"]
            )

            sector = gr.CheckboxGroup(
                choices=["Agriculture", "Aéronautique", "Services aux entreprises", "Chimie", "Conglomérats"],
                label="Secteur"
            )

            stretch_areas = gr.CheckboxGroup(
                choices=["Structuration", "Numéricité", "Jugement & insights", "Créativité", "Leadership de cas"],
                label="Zones de développement"
            )

            with gr.Row():
                submit_button = gr.Button("Soumettre")
                output_space = gr.Label()

        submit_button.click(
            fn=lambda: "Configuration enregistrée !",
            inputs=[language, difficulty, case_type, case_functions, sector, stretch_areas],
            outputs=output_space
        )

demo.queue()
if __name__ == "__main__":
    demo.launch(favicon_path="./data/favicon.ico")

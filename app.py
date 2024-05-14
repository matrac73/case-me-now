import gradio as gr
from services.services import RAG_mistralAI


demo = gr.ChatInterface(
        RAG_mistralAI,
        title="cAIse coach",
        css="footer {visibility: hidden}",
        submit_btn="Envoyer",
        stop_btn="Stop",
        retry_btn="Re-éssayer",
        undo_btn="Retour",
        clear_btn="Nettoyer",
        fill_height="True",
        concurrency_limit=None
        )

demo.launch(favicon_path="./data/favicon.ico")
# demo.launch(favicon_path="./data/favicon.ico", share=True)

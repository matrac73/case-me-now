import gradio as gr
from services.services import fcn, RAG_mistralAI


def strat_case():
    return gr.ChatInterface(
        RAG_mistralAI,
        css="footer {visibility: hidden}",
        submit_btn="Send",
        stop_btn="Stop",
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear",
        fill_height="True",
        concurrency_limit='None'
        )


def data_case():
    inputs = []
    outputs = [
            gr.components.Textbox(label='Your Case'),
            ]

    return gr.Interface(
        fcn,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Calculer",
        clear_btn="Effacer"
        )


def env_case():
    inputs = []
    outputs = [
            gr.components.Textbox(label='Your Case'),
            ]

    return gr.Interface(
        fcn,
        inputs=inputs,
        outputs=outputs,
        css="footer {visibility: hidden}",
        allow_flagging="never",
        submit_btn="Calculer",
        clear_btn="Effacer"
        )


interfaces = [
    strat_case(),
    data_case(),
    env_case()
]


demo = gr.TabbedInterface(
    interface_list=interfaces,
    tab_names=["Strat", "Data", "Env"],
    css="footer {visibility: hidden}",
    title="cAIse coach",
    theme=gr.themes.Base()
    )

demo.launch(favicon_path="./data/favicon.ico")
# demo.launch(favicon_path="./data/favicon.ico", share=True)

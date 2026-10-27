# Case Me Now

**An AI sparring partner for consulting case interviews.** Practice a full strategy case with an interviewer that guides you, challenges your structure and answers your questions — by text or by voice.

## Features

- **Interviewer copilot** – a Mistral-powered interviewer runs the case step by step (context, clarifying questions, framework, quantitative analysis, recommendation), grounded in the case document via retrieval (FAISS + Mistral embeddings).
- **Voice mode** – answer out loud: speech is transcribed with Whisper, and the interviewer's reply can be read back with text-to-speech.
- **Multimodal input** – drop an image (a drawn framework, a calculation) into the chat.
- **Case generator tab** – generate new practice cases.
- Sample cases included in `data/` (Rolling Industries, AJ Chemicals, Sassy Salsa).

## Quick start

```bash
git clone https://github.com/matrac73/case-me-now.git
cd case-me-now
pip install gradio openai mistralai langchain langchain-community langchain-mistralai faiss-cpu pypdf python-dotenv
```

Create a `.env` file:

```env
MISTRALAI_API_KEY=your-mistral-key
OPENAI_API_KEY=your-openai-key   # Whisper (speech-to-text) and TTS
```

Run the app, then open the local URL printed by Gradio:

```bash
python app.py
```

## Project structure

```
app.py               Gradio UI (Copilot and Case generator tabs)
services/
  prompts.py         Interviewer system prompt and case loading
  services.py        LLM inference, speech-to-text, text-to-speech
  utils.py           PDF loading, section splitting, vector store
  theme.py           UI theme
data/                Sample case PDFs
```

## Stack

Python · Gradio · Mistral AI · OpenAI Whisper & TTS · LangChain · FAISS

## License

MIT

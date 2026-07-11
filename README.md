# Medical-ChatBot
# How to run?
### STEPS:
Clone the repository
```bash
git clone https://github.com/radwaelreedy/Medical-ChatBot.git
cd Medical-ChatBot
```
### STEP 01- Create a conda environment after opening the repository 
```bash
conda create -n medibot python=3.10 -y 
```
```bash
conda activate medibot
```
### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```
### STEP 03- Create a `.env` file in the root directory and add the following:
```ini
OPENROUTER_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
FLASK_SECRET_KEY = "your-random-secret-key-here"
```
You can get your API key from [OpenRouter](https://openrouter.ai).
### STEP 04- Build the FAISS vector index by running:
```bash
python store_index.py
```
This will load the PDF data, split it into chunks, generate embeddings, and save a local FAISS index (`faiss_index/`).
### STEP 05- Run the application
```bash
python app.py
```
Now open up your browser and navigate to:
```bash
http://localhost:8080
```
> This applies to local development only. Once deployed on Railway, use the generated public URL instead (see Deployment section below).
---
## Tech Stack Used
- Python
- LangChain
- Flask
- FAISS (vector database)
- Hugging Face Embeddings (sentence-transformers/all-MiniLM-L6-v2)
- OpenRouter (LLM API) — using `anthropic/claude-haiku-4.5`
- Session-based conversation memory (`RunnableWithMessageHistory`)
---
## Features
- Retrieval-Augmented Generation (RAG) over medical PDF documents
- Persistent conversation memory per user session (via Flask session + `uuid`)
- Powered by Claude Haiku 4.5 through OpenRouter
---
## Deployment
This project is deployed on [Railway](https://railway.app):
1. Push your code to GitHub.
2. Create a new **Project** on Railway and connect it to your repository.
3. Railway will detect the Python app automatically. Make sure your **Start Command** is:
```bash
   gunicorn --bind 0.0.0.0:$PORT app:app
```
   (or `python app.py` if not using Gunicorn — see note below)
4. Add the following environment variables in the Railway dashboard (Variables tab):
   - `OPENROUTER_API_KEY`
   - `FLASK_SECRET_KEY`
5. Under **Settings → Networking**, click **Generate Domain** to expose the service publicly.
6. Deploy and access your chatbot via the generated Railway URL.
> **Note:** Make sure `app.py` reads the port dynamically from Railway's `PORT` environment variable instead of a hardcoded port, otherwise the service will show as "Unexposed":
> ```python
> if __name__ == '__main__':
>     port = int(os.environ.get("PORT", 8080))
>     app.run(host="0.0.0.0", port=port, threaded=True)
> ```
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

### STEP 03- Create a `.env` file in the root directory and add your OpenRouter API key as follows:

```ini
OPENROUTER_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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

---

## Tech Stack Used
- Python
- LangChain
- Flask
- FAISS (vector database)
- Hugging Face Embeddings (sentence-transformers/all-MiniLM-L6-v2)
- OpenRouter (LLM API)

---

## Deployment

This project can be deployed on [Render](https://render.com):

1. Push your code to GitHub.
2. Create a new **Web Service** on Render and connect it to your repository.
3. Set the **Build Command**:
```bash
   pip install -r requirements.txt && python store_index.py
```
4. Set the **Start Command**:
```bash
   python app.py
```
5. Add your `OPENROUTER_API_KEY` as an environment variable in the Render dashboard.
6. Deploy and access your chatbot via the generated Render URL.

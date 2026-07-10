from langchain_community.vectorstores import FAISS
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from dotenv import load_dotenv
import os

load_dotenv()
print("✅ Step 1: .env loaded")

openai_api_key = os.environ.get("OPENROUTER_API_KEY")
print("✅ Step 2: API key loaded:", "Found" if openai_api_key else "MISSING!")

extracted_data = load_pdf_file(data='data/')
print("✅ Step 3: PDFs loaded, count:", len(extracted_data))

text_chunks = text_split(extracted_data)
print("✅ Step 4: Text split done, chunks:", len(text_chunks))

embeddings = download_hugging_face_embeddings()
print("✅ Step 5: Embeddings model loaded")

vectorstore = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
print("✅ Step 6: FAISS vectorstore created")

vectorstore.save_local("faiss_index")
print("✅ Step 7: FAISS index saved to disk!")

print("📂 Current working directory:", os.getcwd())
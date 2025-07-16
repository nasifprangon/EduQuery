from flask import Flask, request, jsonify
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load and embed syllabus documents
def load_vectorstore():
    loader1 = TextLoader("syllabus1.txt")
    loader2 = TextLoader("syllabus2.txt")
    documents = loader1.load() + loader2.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = FAISS.from_documents(texts, embeddings)
    return vectordb

vectordb = load_vectorstore()
qa = RetrievalQA.from_chain_type(llm=OpenAI(api_key=openai_api_key), retriever=vectordb.as_retriever())

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    answer = qa.run(question)
    return jsonify({"answer": answer})

@app.route("/")
def home():
    return "EduQuery backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

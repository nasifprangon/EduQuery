from flask import Flask, request, jsonify
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load and embed syllabus documents
def load_vectorstore():
    try:
        loader1 = TextLoader("syllabus1.txt")
        loader2 = TextLoader("syllabus2.txt")
        documents = loader1.load() + loader2.load()

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectordb = FAISS.from_documents(texts, embeddings)
        return vectordb
    except Exception as e:
        print("❌ Error loading documents:", e)
        raise

# Initialize QA pipeline
try:
    vectordb = load_vectorstore()
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(api_key=openai_api_key),
        retriever=vectordb.as_retriever()
    )
except Exception as e:
    print("❌ Failed to initialize QA pipeline:", e)
    qa = None

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    try:
        if not question.strip():
            return jsonify({"answer": "Please enter a valid question."})
        if qa is None:
            return jsonify({"answer": "Backend initialization failed."}), 500
        answer = qa.run(question)
        return jsonify({"answer": answer})
    except Exception as e:
        print("❌ Error during QA run:", e)
        return jsonify({"answer": "Something went wrong: " + str(e)}), 500

@app.route("/")
def home():
    return "EduQuery backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

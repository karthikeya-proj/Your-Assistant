from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SimpleNodeParser
from modules.doc_loader import load_documents

def create_query_engine(filename: str, model: str = "llama3"):
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(model=model)
    Settings.node_parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=50)

    documents = load_documents(filename.replace(".pdf", ".txt"))
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

def ask_query(engine, question: str):
    return engine.query(question)

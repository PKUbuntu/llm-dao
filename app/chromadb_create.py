import chromadb

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Settings

import os
files = os.listdir('./data')

llama_host = "http://" +  os.getenv('OLLAMA_HOST', 'localhost:11434')

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.llm = Ollama(model='qwen2:1.5b', base_url=llama_host, request_timeout=360.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", base_url=llama_host)


for f in files:
    # load some documents
    documents = SimpleDirectoryReader(input_files=["./data/" + str(f)]).load_data()

    # initialize client, setting path to save data
    db = chromadb.PersistentClient(path="./chroma_db")

    # create collection
    chroma_collection = db.get_or_create_collection("vdb_" + str(f))

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    # create a query engine and query
    query_engine = index.as_query_engine()
    response = query_engine.query("What is this article about?")
    print(response)



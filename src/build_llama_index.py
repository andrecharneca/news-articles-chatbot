from llama_index import (VectorStoreIndex, 
                         SimpleDirectoryReader, 
)   
from llama_index.node_parser import SimpleNodeParser
import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARTICLES_JSONS_PATH = os.path.join(ROOT_DIR, "data", "articles")
INDEX_PATH = os.path.join(ROOT_DIR, "data", "articles_llama_index")

def build_index(index_path = INDEX_PATH, articles_jsons_path=ARTICLES_JSONS_PATH):
    # Loading from a directory
    print("Loading documents from ", os.path.abspath(articles_jsons_path))
    documents = SimpleDirectoryReader(ARTICLES_JSONS_PATH).load_data()
    for document in documents:
        #load document.text as json
        json_text = json.loads(document.text)
        document.text = json_text["text"]
        document.metadata = {"title": json_text["title"], "url": json_text["url"], "date": json_text["date"]}
        
    parser = SimpleNodeParser.from_defaults(
        chunk_size=512,
        include_prev_next_rel=False,
    )

    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=index_path)
    print("Index built and saved to ", os.path.abspath(index_path))

def main():
    build_index()

if __name__ == "__main__":
    main()
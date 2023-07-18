
from .prompts import TEXT_QA_TEMPLATE, REFINE_TEMPLATE
from llama_index import (StorageContext, 
                         load_index_from_storage, 
                         ServiceContext)
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.llms import OpenAI
from llama_index.callbacks.schema import CBEventType, EventPayload
from .build_llama_index import INDEX_PATH

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def setup_query_engine():
    chatgpt = OpenAI(model="gpt-3.5-turbo", temperature=0.0)
    service_context = ServiceContext.from_defaults(
        llm = chatgpt,
    )
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    # load index
    index = load_index_from_storage(storage_context, service_context = service_context)
    query_engine = index.as_query_engine(
        similarity_top_k=4,
        text_qa_template=TEXT_QA_TEMPLATE,
        refine_template = REFINE_TEMPLATE,
    )
    return query_engine

def process_article_links(response)->str:
    article_links = ""
    urls = set([node.node.metadata["url"] for node in response.source_nodes])
    for url in urls:
        # get title
        title = [node.node.metadata["title"] for node in response.source_nodes if node.node.metadata["url"] == url][0]
        article_links += f"""<details><summary><a href='{url}' target='_blank'> {title} </a></summary>\n\n"""
        for node in response.source_nodes:
            if node.node.metadata["url"] == url:
                article_links += f"""*{node.node.text}*\n\n"""
        article_links += "</details>\n\n"

    # for node in response.source_nodes:
    #     if node.node.metadata["url"] not in urls:
    #         article_links += f"""<details><summary><a href='{node.node.metadata["url"]}' target='_blank'> {node.node.metadata["title"]} </a></summary>\n\n"""
    return article_links

def get_bot_response(query_engine, user_input)->str:
    # Process the user input and generate a response from the chatbot
    output = "**Related articles:**\n\n{article_links}\n**Answer:**\n\n{answer}"
    response = query_engine.query(user_input)
    article_links = process_article_links(response)
    output = output.format(article_links=article_links, answer=response.response)
    
    return output

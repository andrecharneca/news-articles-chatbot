from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from llama_index.prompts import Prompt

CHAT_TEXT_QA_MSGS = [
    SystemMessagePromptTemplate.from_template(
        "Always answer the question, even if the context isn't helpful. You are helping a business and tech analyst find interesting relationships between companies and products."
    ),
    HumanMessagePromptTemplate.from_template(
        "Passages from news articles below. Use them as context.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the question, always citing relevant and small passages from the articles for every claim you make: {query_str}\n"
    ),
]
CHAT_TEXT_QA_MSGS_LC = ChatPromptTemplate.from_messages(CHAT_TEXT_QA_MSGS)
TEXT_QA_TEMPLATE = Prompt.from_langchain_prompt(CHAT_TEXT_QA_MSGS_LC)

# Refine Prompt
CHAT_REFINE_MSGS = [
    SystemMessagePromptTemplate.from_template(
        "Always answer the question, even if the context isn't helpful. You are helping a business and tech analyst find interesting relationships between companies and products."
    ),
    HumanMessagePromptTemplate.from_template(
        "We have the opportunity to refine the original answer "
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the question, always referencing the articles for your claims: {query_str}. "
        "If the context isn't useful, output the original answer again.\n"
        "Original Answer: {existing_answer}"
    ),
]


CHAT_REFINE_MSGS_LS = ChatPromptTemplate.from_messages(CHAT_REFINE_MSGS)
REFINE_TEMPLATE = Prompt.from_langchain_prompt(CHAT_REFINE_MSGS_LS)
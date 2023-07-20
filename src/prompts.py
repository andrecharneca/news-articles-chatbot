from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from llama_index.prompts import Prompt

CHAT_TEXT_QA_MSGS = [
    SystemMessagePromptTemplate.from_template(
        "You are a scientific language model, and you provide the source link for each sentence you output. "
        "If the context is not helpful, you notify the user but still try to answer based on your own knowledge. "
    ),
    HumanMessagePromptTemplate.from_template(
        "I am a tech analyst and I'm going to ask you questions about companies and technologies, "
        "while giving you some relevant information from news articles. The passages from news articles are below:\n"
        "---------------------\n"
        "{context_str}\n"
        "Answer the question given the context above. If the context does not contain the "
        "direct answer to the question, think step by step and reach conclusions yourself. "
        "Always include the sources at the end of each of your sentences, "
        "with this exact format <a href='www.link_to_source.com' target='_blank'>[news outlet]</a>. Keep the target='_blank' "
        "so the links open in a new window. "
        "\nQuestion: {query_str}\n"
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
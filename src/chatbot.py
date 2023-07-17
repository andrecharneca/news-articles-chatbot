
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

# import logging
# import sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

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
    )
    return query_engine

def get_bot_response(query_engine, user_input):
    # Process the user input and generate a response from the chatbot
    
    # Using the LlamaDebugHandler to print the trace of the sub questions
    # captured by the SUB_QUESTION callback event type
    ## Setup Subquestion Engine ##
    query_engine_tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="news_articles", description="News articles from the web about companies"
            ),
        )
    ]
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager([llama_debug])
    service_context = ServiceContext.from_defaults(callback_manager=callback_manager)
    query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=query_engine_tools,
        service_context=service_context,
    )
    response = query_engine.query(
        user_input,
    )

    # Create an empty list to store the sub questions and answers
    sub_questions_and_answers = []

    # Iterate through the sub questions and answers captured by the SubQuestionQueryEngine
    for start_event, end_event in llama_debug.get_event_pairs(CBEventType.SUB_QUESTIONS):
        for i, qa_pair in enumerate(end_event.payload[EventPayload.SUB_QUESTIONS]):
            sub_questions_and_answers.append(
                {
                    "sub_question": qa_pair.sub_q.sub_question.strip(),
                    "answer": qa_pair.answer.strip(),
                }
            )
    return prepare_bot_output(response, sub_questions_and_answers)

def prepare_bot_output(response, sub_questions_and_answers):
    # Prepare the response from the chatbot to be displayed in the frontend
    output = ""
    for qa in sub_questions_and_answers:
        output += f"**Q:** {qa['sub_question']}  \n**A:** {qa['answer']}  \n"
    output += f"**Final Response:** {response.response}" 
    return output      

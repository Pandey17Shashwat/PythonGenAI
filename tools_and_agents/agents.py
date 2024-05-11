from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import Tool, initialize_agent, create_sql_agent
from langchain_community.utilities import SerpAPIWrapper
import os
from langchain.chains import RetrievalQA
from embeddings.embeddings import vectorstore 
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.utilities import SerpAPIWrapper  
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import SQLDatabase
from typing import Dict

os.environ['GROQ_API_KEY'] ='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'
GROQ_LLM = ChatGroq(model_name='llama3-8b-8192', temperature=0.9)



template = '''
Answer the following question as best you can.
Questions: {question}
'''

prompt_template= PromptTemplate.from_template(template)
prompt=hub.pull('hwchase17/react')


import os
os.environ["SERPAPI_API_KEY"] ='9d4a4736732979038b1947bad8044c67bb97a97994e35ada7d5bd47126ed04a3'
from langchain_community.utilities import SerpAPIWrapper
search = SerpAPIWrapper()


def invoke_llm_and_get_content(query):
    response = GROQ_LLM.invoke(query)
    return (response.content)  # Ensure that 'content' is the correct attribute


llm_tool = Tool(
    name="llm_tool",
    description="Use when pretrained data is useful. Returns only content from LLM",
    func=invoke_llm_and_get_content
)


serpapi_tool = Tool(
    name="serpapi_tool",
    description="if the user query is asking for information regarding IPL",
    func=search.run  # Linking the '.run' method directly
)

# import vectorstore
retriever = vectorstore.as_retriever()
 
qa_chain= RetrievalQA.from_chain_type(
    llm=GROQ_LLM,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)
 
def process_llm_response(llm_response):
    string_ans=""
    string_ans+=llm_response["result"]
    string_ans+='\n\nSources: '
    
    for source in llm_response["source_documents"]:
        string_ans+=source.metadata['source']
        string_ans+='\n'
    return string_ans    
       
def rag_call(query):
    llm_response=qa_chain(query)
    return process_llm_response(llm_response)  


# RAG TOOL


from langchain.agents import Tool


rag_tool = Tool(
    name="rag_tool",
    description="Check the files in the vectorstore and based on that tell if the answer can be given using this",
    func=rag_call
)


DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapidb3"
LLM = GROQ_LLM  # assuming GROQ_LLM is defined elsewhere




################

db = SQLDatabase.from_uri('postgresql+psycopg2://postgres:postgres@localhost/fastapidb3')
print(db)
toolkit = SQLDatabaseToolkit(db=db,llm=GROQ_LLM)

sql_tool = create_sql_agent(
    llm=GROQ_LLM,
    toolkit=toolkit,
    verbose=True
)

def sql_run(query):
    return sql_tool.run(query)

sqlQueryTool = Tool(
    name="sqlQueryTool",
    description="use when input is about any operation related to database",
    func=sql_run,
    verbose=True
)





tools = [llm_tool,serpapi_tool,rag_tool,sqlQueryTool]

from langchain.agents import initialize_agent
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=3,
    return_messages=True
)
conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    prefix='check what the question is asked and how the result should be shown',
    suffix='check the output logically and give the final output by logically implementing the answer',
    llm=GROQ_LLM ,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)


dict=conversational_agent.invoke("highest run scorer of ipl 2023 ?")
chat_history=f'input : {dict.get("input") }  \noutput : {dict.get("output")} '

print(chat_history)
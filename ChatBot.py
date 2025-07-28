from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores.faiss import FAISS
from orm import SessionLocal, Product
from sqlalchemy import text

# get info/documents from the web 
def get_documents_from_web(url):
    loader = WebBaseLoader(url)
    documet = loader.load()
    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 20
    )
    splitdoc =  spliter.split_documents(documet)
    print(len(splitdoc))
    return splitdoc

# create vectorstore
def create_vector(docs):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs,embedding=embedding)
    return vector_store

# create retrieval chain
def create_chain(vector_store):
    api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name='llama-3.1-8b-instant'  
    )

    # System prompt for SQL generation
    template = '''
    You are a helpful assistant for a product database. If the user's question requires data from the database, generate a valid SQL query for PostgreSQL using the 'products' table with columns: ProductKey, Product_Name, Brand, Color, Unit_Cost_USD, Unit_Price_USD, SubcategoryKey, Subcategory, CategoryKey, Category. Otherwise, answer normally.

    context: {context}
    User: {input}
    '''

    prompt = ChatPromptTemplate.from_template(template)
    chain = create_stuff_documents_chain(
        llm= llm,
        prompt= prompt
    )

    retreiver = vector_store.as_retriever(search_kwargs={'k':2})
    reteivel_chain = create_retrieval_chain(
        retreiver,
        chain,
    )

    return reteivel_chain, llm

def execute_sql_query(sql_query):
    session = SessionLocal()
    try:
        result = session.execute(text(sql_query))
        rows = result.fetchall()
        columns = result.keys()
        session.close()
        # Format as list of dicts
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        session.close()
        return f"SQL execution error: {e}"

def is_sql_query(text):
    sql_keywords = ['select', 'update', 'delete', 'insert']
    return any(text.strip().lower().startswith(k) for k in sql_keywords)

def chatbot_respond(user_input, chain, llm):
    # First, get the LLM's response
    response = chain.invoke({'input': user_input})
    answer = response.get('output', '') or response.get('context', '')
    # If the LLM generated a SQL query, execute it
    if is_sql_query(answer):
        sql_result = execute_sql_query(answer)
        return sql_result
    else:
        return answer



# vector store
vectore_store = create_vector(doc)
# retrieval chain and llm
chain, llm = create_chain(vectore_store)

# Example usage
user_prompt = input("Ask your question: ")
result = chatbot_respond(user_prompt, chain, llm)
print(result)
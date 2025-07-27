from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import HumanMessage,AIMessage  
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever


#Load documents from a web URL
def get_documents_from_web(url):
    loader = WebBaseLoader(url)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20
    )
    split_docs = splitter.split_documents(documents)
    print(f"split {len(split_docs)} documents.")
    return split_docs

#Create FAISS vector store with HuggingFace embeddings
def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs, embedding=embeddings)
    return vector_store

#Create LangChain Retrieval Chain (Retriever + LLM)
def create_chain(vector_store):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama3-8b-8192"
    )

    template = """
    Answer the user's question as best as you can using the context below.

    Context:
    {context}

    User Question:
    {input}
    """
    #added chathistory with human and ai 
    prompt = ChatPromptTemplate.from_messages([
        ('system', "Answer the user's question as best as you can using the context: {context}"),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}')
    ])

    #Stuff the documents into the LLM with the prompt
    doc_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("human", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
  

    ])

    #Create a history-aware retriever so the chatbot becomes more efficient and responds appropriately based on the user's input
    history_aware_retriver = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=retriever_prompt
    )
    #Create full retrieval-augmented generation chain
    reteivel_chain = create_retrieval_chain(
        retriever=history_aware_retriver,
        combine_docs_chain=doc_chain
    )

    return reteivel_chain


def procces_chat(chain,question,chat_history):
    #Ask a question
    response = chain.invoke({"input":question,
                             'chat_history':chat_history})

    # Step 5: Print final answer
    return response["answer"]


# === RUN EVERYTHING ===

#Load web documents
docs = get_documents_from_web("https://python.langchain.com/docs/concepts/lcel/")

#Create vector store
vector_store = create_vector_store(docs)

#Create chain
chain = create_chain(vector_store)

chat_history = []
#user can now question in the terminal 
while True:
    user = input('You: ')
    if user.lower() == 'exit':
        break
    response = procces_chat(chain,user,chat_history)
    chat_history.append(HumanMessage(content=user))
    chat_history.append(AIMessage(content=response))
    print(f'Chatbot: {response}')
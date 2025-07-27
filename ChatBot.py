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

#get info/documets from the web 
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


#create vectorestore
def create_vector(docs):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs,embedding=embedding)
    return vector_store

#create retrival chain
def create_chain(vector_store):
    api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name='llama3-8b-8192'  
    )

    template = '''
    answer the user questions

    context: {context}
    User: {input}


    '''

    prompt = ChatPromptTemplate.from_template(template)

    # chain = prompt | llm
    chain = create_stuff_documents_chain(
        llm= llm,
        prompt= prompt
        )

    retreiver = vector_store.as_retriever(search_kwargs={'k':2}) #returns relevent documents, can be set to how ever documents user wants > search_kwargs={'k':2} 2 relevents documents will be returned
    reteivel_chain = create_retrieval_chain(
        retreiver,
        chain,
    )

    return reteivel_chain


#doc from web
doc = get_documents_from_web('https://python.langchain.com/docs/concepts/lcel/')

#vectore store
vectore_store = create_vector(doc)

#retrival chain
chain = create_chain(vectore_store)




response = chain.invoke({'input':'what is LCEL',
                         })

print(response['context'])
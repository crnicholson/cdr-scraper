from funcs import *
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Loading orca-mini from Ollama
llm = Ollama(model="llama3", temperature=0)

# Loading the Embedding Model
embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# loading and splitting the documents
docs = load_pdf_data(file_path="papers/0feedb41-a9b8-4ff7-b360-a1795ec8ac3b.pdf")
documents = split_docs(documents=docs)

# creating vectorstore
vectorstore = create_embeddings(documents, embed)

# converting vectorstore to a retriever
retriever = vectorstore.as_retriever()

# Creating the prompt from the template which we created before
prompt = PromptTemplate.from_template(template)

# Creating the chain
chain = load_qa_chain(retriever, llm, prompt)

get_response("Summarize this research paper", chain)

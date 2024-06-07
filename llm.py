import os
from langchain_community.llms import Ollama
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Step 1: Load all PDFs from a folder and extract the text
folder_path = "/Users/Charlie/Documents/Code/webScraper/papers"
documents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_loader = PyPDFLoader(file_path=os.path.join(folder_path, filename))
        documents.extend(pdf_loader.load())

# Step 2: Create a retriever from the extracted text
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Step 3: Use the retriever in combination with the language model to perform the query
llm = Ollama(model="llama3")
qa_chain = RetrievalQA(llm=llm, retriever=retriever)

# Step 4: Perform the query
response = qa_chain.run("Summarize carbon dioxide removal technologies.")
print(response)

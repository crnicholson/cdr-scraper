import fitz  # PyMuPDF library for extracting text from PDFs
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Function to answer questions based on PDF content
def answer_question_from_pdf(pdf_path, question):
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Initialize the chat model
    chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")

    # Define the system and human messages
    system = (
        "You are a helpful assistant. Answer the questions based on the provided text."
    )
    human = f"Context: {pdf_text}\n\nQuestion: {question}"

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    # Create the chain and invoke it with the question
    chain = prompt | chat
    return chain.invoke({"text": human})


# Example usage
pdf_path = "papers/3706709c-9c5a-4b21-9969-22a453f84d18.pdf"
question = "Explain this article."
print(answer_question_from_pdf(pdf_path, question))

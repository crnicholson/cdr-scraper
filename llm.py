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
    chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

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
pdf_path = "papers/553a2d1a-196c-4a3d-9994-c6be19db78cc.pdf"
question = "Explain community engagement in CDR."
print(answer_question_from_pdf(pdf_path, question))

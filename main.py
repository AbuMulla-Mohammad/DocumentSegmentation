from pydantic import BaseModel
from models.structured_document import StructuredDocument
from utils.document_processing import doc_with_lines
import cohere
import instructor
from docx import Document
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv('COHERE_API_KEY')

if not api_key:
    raise ValueError("API key for Cohere is not set in the .env file.")

# Initialize the cohere client with the API key
client = cohere.Client(api_key)

# Apply the patch to the cohere client
# Enables response_model keyword
client = instructor.from_cohere(client)

system_prompt = """\
You are a world class educator working on organizing your lecture notes.
Read the document below and extract a StructuredDocument object from it where each section of the document is centered around a single concept/topic that can be taught in one lesson.
Each line of the document is marked with its line number in square brackets (e.g. [1], [2], [3], etc). Use the line numbers to indicate section start and end.
"""

def get_structured_document(document_with_line_numbers: str) -> StructuredDocument:
    response = client.chat.completions.create(
        model="command-r-plus",
        response_model=StructuredDocument,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": document_with_line_numbers,
            },
        ],
    )  # type: ignore
    return response

def get_sections_text(structured_doc: StructuredDocument, line2text: dict) -> list:
    segments = []
    for s in structured_doc.sections:
        contents = [line2text.get(line_id, '') for line_id in range(s.start_index, s.end_index)]
        segments.append({
            "title": s.title,
            "content": "\n".join(contents),
            "start": s.start_index,
            "end": s.end_index
        })
    return segments

def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# Prompt for user input for DOCX file
docx_path = 'C:/Users/BisanCo/Desktop/intern materials/ML-Models/Document Segmentation 2/files/Mohammed Burhan Abu MuallaCV.docx'

# Extract text from the DOCX file
try:
    document = extract_text_from_docx(docx_path)
    document_with_line_numbers, line2text = doc_with_lines(document)
    structured_doc = get_structured_document(document_with_line_numbers)
    segments = get_sections_text(structured_doc, line2text)

    # Print the results
    print("Structured Document:")
    # Use .dict() and convert to JSON manually if necessary
    print(structured_doc.dict())

    print("\nSegments:")
    for segment in segments:
        print(f"Title: {segment['title']}")
        print(f"Start: {segment['start']}")
        print(f"End: {segment['end']}")
        print("Content:")
        print(segment['content'])
        print("-" * 40)  # Separator between segments

except Exception as e:
    print(f"An error occurred: {e}")

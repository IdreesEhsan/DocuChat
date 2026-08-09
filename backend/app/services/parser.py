import PyPDF2
import docx
from fastapi import UploadFile
import io

async def parse_file(file: UploadFile):
    content = await file.read()
    metadata = {"source": file.filename}
    text = ""

    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        for i, page in enumerate(reader.pages):
            text += page.extract_text() + "\n"
        metadata["total_pages"] = len(reader.pages)
        return text, metadata

    elif file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text, metadata

    raise ValueError("Unsupported file type. Use PDF or DOCX.")
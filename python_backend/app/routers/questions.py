from fastapi import APIRouter, HTTPException
from app.services.rag_model import mock_rag_model
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import os

router = APIRouter()

UPLOAD_DIR = "./uploaded_files"

@router.get("/ask/")
async def ask_question(question: str):
    file_path = f"{UPLOAD_DIR}/parsed_data.md"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # load the parsed data
    loader = UnstructuredMarkdownLoader(file_path)
    loaded_documents = loader.load()

    # Split the parse data into chunks, the chunk size is 512 characters
    # This parameter is very important, it will affect the performance of the model
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=20)
    splits = text_splitter.split_documents(loaded_documents)

    # Embed
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()
    answer = mock_rag_model(question, retriever)

    return {"answer": answer}


# import libraries
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI, File, UploadFile

import os
import io

app = FastAPI()

origins = [
    "*"
]

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = "https://docs-reader-assignment.cognitiveservices.azure.com/"
key = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    image_data = await file.read()

    poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", image_data)
    result = poller.result()

    return {
        "filename": file.filename,
        "analysis_result": result.content
    }

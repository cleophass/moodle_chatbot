from langchain_community.embeddings.ollama import OllamaEmbeddings
import streamlit as st
from functions import *
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import os
CHROMA_PATH = "chroma"
DATA_PATH = "data"


# Définition du template de prompt
PROMPT_TEMPLATE = """
Répondez à la question en vous basant uniquement sur le contexte suivant :
{context}

---
Répondez à la question en vous basant sur le contexte ci-dessus : {question}
"""

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings



def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Recherche dans la base de données
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    # Extraire uniquement le nom du fichier sans le chemin et le chunk
    sources = list(set([os.path.basename(doc.metadata.get("id", "")) for doc, _score in results]))
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return response_text, sources

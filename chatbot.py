import streamlit as st
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import os
import re

CHROMA_PATH = "chroma"
DATA_PATH = "data"

PROMPT_TEMPLATE = """
Répondez à la question en vous basant uniquement sur le contexte suivant :
{context}

---
Répondez à la question en vous basant sur le contexte ci-dessus : {question}
"""

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def preprocess_source(source):
    # Extraction de la partie lisible du chemin
    match = re.search(r'/([^/]+\.pdf)', source)
    return match.group(1).replace('_', ' ') if match else source

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

    sources = list(set([preprocess_source(doc.metadata.get("id", "")) for doc, _score in results]))
    return response_text, sources

# Interface Streamlit
def main():
    st.set_page_config(page_title="Chatbot RAG", layout="wide")
    st.title("💬 Chatbot RAG avec Streamlit")

    # Stockage des messages dans la session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affichage de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Champ de saisie utilisateur
    query_text = st.chat_input("Envoyez votre message...")
    if query_text:
        # Ajout du message utilisateur
        st.session_state.messages.append({"role": "user", "content": query_text})
        with st.chat_message("user"):
            st.markdown(query_text)

        # Obtenir la réponse du LLM
        response_text, sources = query_rag(query_text)

        # Affichage des sources en badges horizontaux
        st.markdown("**Sources utilisées:**")
        st.markdown(" ".join([f"`{source}`" for source in sources]))

        # Ajout du message de l'assistant
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)

if __name__ == "__main__":
    main()

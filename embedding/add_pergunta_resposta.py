import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from settings import BANCO_FAISS_PATH, embeddings
import json



def adicionar_pergunta_resposta(pergunta: str, resposta: str):
    

    # Tenta carregar o banco existente
    if os.path.exists(BANCO_FAISS_PATH):
        try:
            vectorstore = FAISS.load_local(
                BANCO_FAISS_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print("Erro ao carregar FAISS existente:", e)
            vectorstore = None
    else:
        vectorstore = None

    # Se não existir, cria um novo
    if vectorstore is None:
        vectorstore = FAISS.from_texts(
            [pergunta],
            embedding=embeddings,
            metadatas=[{"resposta": resposta}]
        )
    else:
        vectorstore.add_texts(
            [pergunta],
            metadatas=[{"resposta": resposta}]
        )

    # Salva o banco atualizado
    vectorstore.save_local(BANCO_FAISS_PATH)
    print("Pergunta e resposta adicionadas com sucesso!")

if __name__ == "__main__":
    with open(str(Path(__file__).parent / "perguntas.json"), "r") as f:
        conteudo = f.read()
        dados = json.loads(conteudo)
        for item in dados:
            adicionar_pergunta_resposta(item["pergunta"], item["resposta"])        

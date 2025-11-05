from langchain_community.vectorstores import FAISS

from settings import BANCO_FAISS_PATH
from settings import embeddings

def fazer_pergunta(pergunta: str):
    vectorstore = FAISS.load_local(
        BANCO_FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    resultados, score = vectorstore.similarity_search_with_score(pergunta, search_type='similarity', k=1)[0]
    print(score, resultados)
    

if __name__ == "__main__":
    pergunta = input("Digite a pergunta: ")
    fazer_pergunta(pergunta)
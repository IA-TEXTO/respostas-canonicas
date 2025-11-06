import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

nlp = spacy.load("pt_core_news_md")

# classes “de conteúdo” (não precisamos PRON/DET aqui)
CONTENT_POS = {"NOUN", "PROPN", "VERB", "ADJ"}
AUX_DEPS = {"aux", "cop"}

# interrogativos (remoção geral, mas preservamos se for o 1º token “útil”)
WH_WORDS = {
    "qual", "quais", "que", "quem", "quando", "como", "onde",
    "por", "porque", "porquê", "por quê", "por que",
    "quanto", "quantos", "quanta", "quantas"
}
ALL_STOPWORDS = STOP_WORDS.union(WH_WORDS)

def filtra(pergunta: str):
    doc = nlp(pergunta)

    # preservar interrogativo inicial se houver
    leading_wh = None
    for tok in doc:
        if tok.is_space or tok.is_punct:
            continue
        if tok.lower_ in WH_WORDS:
            leading_wh = tok.text  # mantém capitalização
        break

    termos = []
    vistos = set()
    for tok in doc:
        if tok.is_space or tok.is_punct:
            continue
        if tok.lower_ in ALL_STOPWORDS:
            continue
        if tok.pos_ not in CONTENT_POS:
            continue
        if tok.pos_ == "AUX" or tok.dep_ in AUX_DEPS:
            continue

        termo = tok.lemma_.lower() if tok.pos_ != "PROPN" else tok.text
        if termo not in vistos:
            vistos.add(termo)
            termos.append(termo)

    if leading_wh:
        termos = [leading_wh] + termos
    return termos

pergunta = input("Pergunta: ").strip()
resposta = " ".join(filtra(pergunta))
print("Resposta:", resposta)

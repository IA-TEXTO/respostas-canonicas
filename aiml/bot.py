# ---- compat com libs antigas que usam time.clock ----
import time as _time
if not hasattr(_time, "clock"):
    _time.clock = _time.perf_counter  # ou _time.process_time
# -----------------------------------------------------

import aiml, glob, os, unicodedata

def normalize(txt: str) -> str:
    # remove acentos e deixa maiúsculo (AIML casa melhor assim)
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    return txt.upper()

kernel = aiml.Kernel()


for path in glob.glob(os.path.join(os.path.dirname(__file__), "*.aiml")):
    kernel.learn(path)

print("Bot pronto. Digite algo (CTRL+C para sair).")
while True:
    user = input("Você: ")
    reply = kernel.respond(normalize(user)) or "Não entendi. Pode reformular?"
    print("Bot:", reply)

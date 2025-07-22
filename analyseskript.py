import requests
import spacy
import json

# ---------- 1. Simulierter Whisper-Output ----------
transkript = """
Weil wir gemerkt haben, dass der August ganz schön voll ist. So bezüglich Kunden Onboarding und so genau. sonst ich tatsächlich beim Finanzplan. Gestern hab ich noch 'n paar Sachen gefixt weil ich Spalten gelöscht hab die unnötig waren das fand er natürlich nur so Medium geil. Deswegen musste ich ein paar Formeln wieder fixen und bin jetzt gerade bei Customer Acquisition Cost dabei die zu berechnen. Das ist auch Das ist wirklich auch ein nerviger aberzogen Genau das gestern aber komm ich irgendwie voran. Hab heute den ganzen Tag mit Leuten rum telefoniert vor allem auch mit Leon noch mal über Fundraising die haben hat mir von so 'n Outreach Tour erzählt, was sie jetzt Woodpacker heißt das kann ich auch noch weiterleiten. ansonsten genau fand ich immer interessant. 
"""

# ---------- 2. Vorverarbeitung mit spaCy ----------
nlp = spacy.load("de_core_news_sm")
doc = nlp(transkript)
personen = [ent.text for ent in doc.ents if ent.label_ == "PER"]
daten = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

print("Erkannte Personen:", personen)
print("Erkannte Daten:", daten)

# ---------- 3. Prompt für das LLM ----------
prompt = f"""
Du bekommst ein Gesprächsprotokoll. Extrahiere:
- To-Dos mit verantwortlicher Person
- Fristen (z.B. Zeitpunkte)
- Erwähnte Themen oder technische Begriffe
- Offene Fragen

Antworte auf Deutsch im JSON-Format.

Text: \"\"\"{transkript}\"\"\"
"""

# ---------- 4. Anfrage an Ollama (lokal) ----------
def query_ollama(prompt, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

antwort_roh = query_ollama(prompt)

# ---------- 5. Versuche, JSON aus der Antwort zu extrahieren ----------
try:
    start = antwort_roh.index("{")
    ende = antwort_roh.rindex("}") + 1
    ergebnis = json.loads(antwort_roh[start:ende])
except Exception as e:
    ergebnis = {"error": str(e), "raw_output": antwort_roh}

# ---------- 6. Ausgabe ----------
print("\n Extraktionsergebnis:")
print(json.dumps(ergebnis, indent=2, ensure_ascii=False))

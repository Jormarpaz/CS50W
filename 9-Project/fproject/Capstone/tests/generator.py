import fitz  # PyMuPDF para PDFs
import docx
import nltk
import random

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Descargar recursos de NLTK si no están descargados
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")

def extract_text_from_file(file_path):
    """Extrae texto de un archivo PDF, DOCX o TXT."""
    text = ""
    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    return text

def extract_key_phrases(text, num_phrases=10):
    """Extrae frases clave del texto para generar preguntas."""
    words = word_tokenize(text)  # Tokeniza las palabras
    words = [word for word in words if word.isalnum()]  # Elimina signos de puntuación

    stop_words = set(stopwords.words("spanish"))  # Filtra palabras vacías
    filtered_words = [word for word in words if word.lower() not in stop_words]

    tagged_words = pos_tag(filtered_words)  # Etiqueta gramaticalmente las palabras
    nouns = [word for word, tag in tagged_words if tag.startswith("NN")]  # Filtra sustantivos

    return random.sample(nouns, min(num_phrases, len(nouns)))  # Selecciona frases aleatorias

def generate_questions(text, num_questions=5):
    """Genera preguntas reemplazando frases clave en el texto."""
    sentences = sent_tokenize(text)  # Divide el texto en oraciones
    key_phrases = extract_key_phrases(text, num_questions)  # Extrae frases clave

    questions = []
    for phrase in key_phrases:
        for sentence in sentences:
            if phrase in sentence:
                question = sentence.replace(phrase, "________")  # Reemplaza la palabra clave
                questions.append(f"¿Qué palabra falta en esta frase?: {question}")
                break  # Solo una pregunta por frase clave

    return questions[:num_questions]  # Devuelve el número de preguntas solicitado

# 🔹 Prueba el código
if __name__ == "__main__":
    texto = extract_text_from_file("ejemplo.pdf")  # Cambia por un archivo real
    preguntas = generate_questions(texto, 5)
    for i, pregunta in enumerate(preguntas, 1):
        print(f"{i}. {pregunta}")


import fitz  # PyMuPDF para PDFs
import docx
import nltk
import random

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag

# Descargar recursos de NLTK si no están descargados
nltk.download('omw-1.4')
nltk.download("wordnet")
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

def generate_wrong_options(correct_word, num_options=3):
    """Genera opciones incorrectas basadas en sinónimos y palabras similares."""
    wrong_options = set()

    # Obtener sinónimos y palabras similares
    for syn in wordnet.synsets(correct_word, lang="spa"):  
        for lemma in syn.lemmas("spa"):
            word = lemma.name().replace("_", " ")  # Reemplazar "_" por espacios
            if word.lower() != correct_word.lower():
                wrong_options.add(word)

    # Si no hay suficientes sinónimos, añadir palabras similares del WordNet
    if len(wrong_options) < num_options:
        related_words = [syn.name().split(".")[0] for syn in wordnet.synsets(correct_word, lang="spa")]
        wrong_options.update(related_words)

    # Si aún faltan opciones, añadir palabras aleatorias (usando sustantivos comunes en español)
    common_words = ["casa", "libro", "puerta", "coche", "ciudad", "nube", "montaña", "árbol"]
    while len(wrong_options) < num_options:
        random_word = random.choice(common_words)
        if random_word.lower() != correct_word.lower():
            wrong_options.add(random_word)

    return list(wrong_options)[:num_options]


def generate_questions(text, num_questions=5):
    """Genera preguntas reemplazando frases clave en el texto."""
    sentences = sent_tokenize(text)  # Divide el texto en oraciones
    key_phrases = extract_key_phrases(text, num_questions)  # Extrae frases clave

    questions = []
    for i, phrase in enumerate(key_phrases):
        for sentence in sentences:
            if phrase in sentence:
                question_text = sentence.replace(phrase, "________")
                
                # Obtener opciones incorrectas
                wrong_options = generate_wrong_options(phrase, 3)
                
                options = [{'id': 1, 'text': phrase, 'is_correct': True}] + \
                          [{'id': i+2, 'text': opt, 'is_correct': False} for i, opt in enumerate(wrong_options)]
                
                random.shuffle(options)
                questions.append({'id': i, 'text': question_text, 'options': options})
                break  

    return questions[:num_questions]  # Devuelve el número de preguntas solicitado

# 🔹 Prueba el código
if __name__ == "__main__":
    texto = extract_text_from_file("ejemplo.pdf")  # Cambia por un archivo real
    preguntas = generate_questions(texto, 5)
    for i, pregunta in enumerate(preguntas, 1):
        print(f"{i}. {pregunta}")


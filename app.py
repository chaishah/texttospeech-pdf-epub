import streamlit as st
import os
from PyPDF2 import PdfReader
from ebooklib import epub
from gtts import gTTS
from tempfile import NamedTemporaryFile
import time

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_epub(file):
    book = epub.read_epub(file)
    text = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text += item.content.decode("utf-8")
    return text

def save_audio(text, language):
    audio = gTTS(text=text, lang=language, slow=False)
    audio_file = NamedTemporaryFile(delete=False)
    audio.save(audio_file.name)
    return audio_file

st.title("PDF & EPUB to Speech")

file = st.file_uploader("Upload a PDF or EPUB file", type=["pdf", "epub"])

if file:
    st.subheader("File Details")
    st.write(f"File Name: {file.name}")
    st.write(f"File Type: {file.type}")

    if file.type == "application/pdf":
        text = read_pdf(file)
    elif file.type == "application/epub+zip":
        text = read_epub(file)

    st.subheader("Text")
    st.write(text)

    language = st.selectbox("Select language for text-to-speech", ["en", "es", "fr", "de", "it", "pt", "zh-cn", "ja", "ko"])

    audio_file = save_audio(text, language)
    audio_file_path = audio_file.name

    st.audio(audio_file_path, format="audio/mp3")

    progress_bar = st.progress(0)
    status_text = st.empty()
    stop_button = st.button("Stop")

    for i in range(100):
        if stop_button:
            break
        time.sleep(0.1)
        status_text.text(f"Playing audio {i + 1}%")
        progress_bar.progress(i + 1)
        if i == 99:
            status_text.text("Audio finished")
            break

    os.unlink(audio_file_path)

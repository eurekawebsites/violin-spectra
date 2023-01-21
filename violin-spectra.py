import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from translate import Translator

st.title("Scientific Paper Summary Generator")

doi = st.text_input("Enter DOI of the paper:")

if doi:
    paper = requests.get(doi).content
    soup = BeautifulSoup(paper, 'html.parser')
    text = soup.get_text()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 5)
    st.write("Summary of the paper:")
    for sentence in summary:
        st.write(sentence)
    st.write("Translations")
    target_languages = ['fr','es','de']
    for lang in target_languages:
        translator= Translator(to_lang=lang)
        translation = translator.translate(" ".join(str(sentence) for sentence in summary))
        st.write(f'Summary in {lang} : {translation}')

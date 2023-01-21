import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import googletrans

st.title("Scientific Paper Summary Generator")

# Use the CrossRef API to retrieve the paper's URL based on the DOI
doi = st.text_input("Enter DOI of the paper:")
headers = {'accept': 'application/vnd.citationstyles.csl+json'}
res = requests.get(f'https://api.crossref.org/works/{doi}', headers=headers)
url = res.json()['message']['URL']

# Scrape the paper's text and summarize it
paper = requests.get(url).content
soup = BeautifulSoup(paper, 'html.parser')
text = soup.get_text()
parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = LexRankSummarizer()
summary = summarizer(parser.document, 5)
st.write("Summary of the paper:")
for sentence in summary:
    st.write(sentence)

# Translate the summary into multiple languages using the googletrans library
st.write("Translations")
target_languages = ['fr','es','de']
for lang in target_languages:
    translator= googletrans.Translator()
    translation = translator.translate(" ".join(str(sentence) for sentence in summary), dest=lang)
    st.write(f'Summary in {lang} : {translation.text}')

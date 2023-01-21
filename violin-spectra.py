import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

st.title("Scientific Paper Summary Generator")

doi = st.text_input("Enter DOI of the paper:")

if doi:
    headers = {'accept': 'application/vnd.citationstyles.csl+json'}
    res = requests.get(f'https://api.crossref.org/works/{doi}', headers=headers)
    if res.status_code != 200:
        st.write("An error occured: ", res.text)
    else:
        try:
            url = res.json()['message']['URL']
            paper = requests.get(url)
            if paper.status_code != 200:
                st.write("An error occured: ", paper.text)
            else:
                soup = BeautifulSoup(paper.content, 'html.parser')
                text = soup.get_text()
                parser = PlaintextParser.from_string(text, Tokenizer("english"))
                summarizer = LexRankSummarizer()
                summary = summarizer(parser.document, 5)
                st.write("Summary of the paper:")
                for sentence in summary:
                    st.write(sentence)
        except ValueError as e:
            st.write("An error occured: Invalid response, response is not in json format")
            raise SystemExit

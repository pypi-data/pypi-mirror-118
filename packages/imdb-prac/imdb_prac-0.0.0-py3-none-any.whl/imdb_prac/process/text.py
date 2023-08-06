import re
import spacy

#build spacy model for procees text
spacy.require_gpu()
en_nlp=spacy.load("en_core_web_md")


#replace html element in context
NonHtml=re.compile(r"<[^<]+?>|<!--.*?-->|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

def strip_html(text):
    text=NonHtml.sub("",text)
    return text
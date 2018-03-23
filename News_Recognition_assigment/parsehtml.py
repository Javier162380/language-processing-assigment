from bs4 import BeautifulSoup
import os
import codecs
from textblob import TextBlob



def parse_html_to_english(path_html,path_txt):
    path=path_html
    for i in os.listdir(path):
       if i.endswith('.html'):
           with codecs.open("{0}{1}".format(path,i),"r",encoding='utf-8', errors='ignore') as raw_html:
               html=raw_html.read()
           Document=BeautifulSoup(html, 'html.parser')
           text=[sentence.get_text() for sentence in Document.findAll("p")]
           raw_text='\n'.join(sentence for sentence in text)
           if TextBlob(raw_text).detect_language() != 'en':
               translated_text=TextBlob(raw_text).translate(to='en').string
               with open('{0}{1}.txt'.format(path_txt,i),'w') as file:
                   file.write((translated_text))
           else:
               with open('{0}{1}.txt'.format(path_txt,i),'w') as file:
                   file.write(raw_text)

if __name__ == '__main__':
    parse_html_to_english('./CorpusNoticiasPractica2018/','./Txt/')
# -*- coding: utf-8 -*-

import glob, os, time, re, sys
from unicodedata import normalize
import xml.etree.ElementTree as ET #library to read xml in python, structure-comprehensible

def NORM(nome): #function to remove strange characters and accents
    nome=normalize('NFKD', nome.decode('utf-8')).encode('ASCII','ignore')
    nome=re.sub('ã|Ã|â|Â|á|Á|à|À','A',nome)
    nome=re.sub('ê|Ê|é|É|è|È','E',nome)
    nome=re.sub('î|Î|í|Í|ì|Ì|ï|Ï','I',nome)
    nome=re.sub('õ|Õ|ô|Ô|ó|Ó|ò|Ò','O',nome)
    nome=re.sub('û|Û|ú|Ú|ù|Ù|ü|Ü','U',nome)
    nome=re.sub('ç|Ç','C',nome)
    nome=re.sub('ñ|Ñ','N',nome)
    nome=re.sub("'",' ',nome)
    nome=re.sub('"',' ',nome)
    nome=nome.replace('*','')
    nome=nome.replace('\\','')
    nome=nome.replace('ª','')
    nome=nome.replace('°','')
    nome=nome.replace('º','')    
    return str(nome)

#recebe o nome do arquivo via CLI
nome_arquivo = sys.argv[1];

print ("article_id\tato\tdata\torgao\tart_name\tart_idOficio\tart_pubName\tart_artClass\tart_artSection\tart_artSize\tart_artNotes\tart_numberPage\tart_pdfPage\tart_editionNumber\tart_texto")

tree = ET.parse(nome_arquivo)

#root is XML tag
root = tree.getroot()           #xml tag

#para cada artigo no DOU
for article in root:

    article_id = article.attrib['id'].encode('utf-8')
    ato = article.attrib['artType'].encode('utf-8')
    data = article.attrib['pubDate'].encode('utf-8')
    orgao = article.attrib['artCategory'].encode('utf-8')
    art_name = article.attrib['name'].encode('utf-8')
    
    try:
        art_idOficio = article.attrib['idOficio'].encode('utf-8')
    except Value:
        art_idOficio = 'null'

    art_pubName = article.attrib['pubName'].encode('utf-8')
    art_artClass = article.attrib['artClass'].encode('utf-8')

    try:
        art_artSection = article.attrib['artSection'].encode('utf-8')
    except KeyError:
        art_artSection = 'null'

    art_artSize = article.attrib['artSize'].encode('utf-8')
    art_artNotes = article.attrib['artNotes'].encode('utf-8')
    art_numberPage = article.attrib['numberPage'].encode('utf-8')
    art_pdfPage = article.attrib['pdfPage'].encode('utf-8')
    art_editionNumber = article.attrib['editionNumber'].encode('utf-8')
    art_texto = article[0][5].text.encode('utf-8')

    print ( article_id + '\t' +
            ato + '\t' +
            data + '\t' +
            orgao + '\t' +
            art_name + '\t' +
            art_idOficio + '\t' +
            art_pubName + '\t' +
            art_artClass + '\t' +
            art_artSection + '\t' +
            art_artSize + '\t' +
            art_artNotes + '\t' +
            art_numberPage + '\t' +
            art_pdfPage + '\t' +
            art_editionNumber + '\t' +
            art_texto) #output
    #arq_saida.write(temp+'\n')

#arq_saida.close()

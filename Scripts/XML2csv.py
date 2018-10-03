# -*- coding: utf-8 -*-

from sys import argv
from re import sub as RegexSub
from re import findall as RegexFindAll
import xml.etree.ElementTree as ET #library to read xml in python, structure-comprehensible

#recebe o nome do arquivo via CLI
nome_arquivo = argv[1];

#function to remove strange characters and accents
def NORM(nome):
    nome=RegexSub('Á|À|Â|Ä|Ã','A',nome)
    nome=RegexSub('á|à|â|ä|ã','a',nome)
    nome=RegexSub('É|È|Ê|Ë','E',nome)
    nome=RegexSub('é|è|ê|ë','e',nome)
    nome=RegexSub('Í|Ì|Î|Ï','I',nome)
    nome=RegexSub('í|ì|î|ï','i',nome)
    nome=RegexSub('Ó|Ò|Ô|Ö|Õ','O',nome)
    nome=RegexSub('ó|ò|ô|ö|õ','o',nome)
    nome=RegexSub('Ú|Ù|Û|Ü','U',nome)
    nome=RegexSub('ú|ù|û|ü','u',nome)
    nome=RegexSub("\'|\"|\*|\\|ª|º|º",' ',nome)
    nome=nome.replace('ç','c')
    nome=nome.replace('Ç','C')
    nome=nome.replace('ñ','n')
    nome=nome.replace('Ñ','N')
    return str(nome)

class Artigo:
    
    #Atributos do artigo
    artCategory='null'      #orgao
    artClass='null'
    artNotes='null'
    artSection='null'
    artSize='null'
    artType='null'          #ato
    editionNumber='null'
    id='null'
    idOficio='null'
    idMateria='null'
    highlight='null'
    highlightPriority='null'
    highlightType='null'
    name='null'
    numberPage='null'
    pdfPage='null'
    pubDate='null'          #data
    pubName='null'
    
    #Informações extras
    qtdParagrafos='null'
    qtdTermos='null'

    #Tags filhas do artigo
    Autores='null'
    Data='null'
    Ementa='null'
    Identifica='null'
    SubTitulo='null'
    Texto='null'
    Titulo='null'


#root is XML tag
tree = ET.parse(nome_arquivo)
root = tree.getroot()           #xml tag

local_artigo = Artigo()
listaAttributos = [a for a in dir(local_artigo) if not a.startswith('__') and not callable(getattr(local_artigo,a))]

# Fazendo o cabecalho
outputString=''
for atributo in listaAttributos:
    outputString += atributo + "\t"

#Imprimindo o cabecalho
print outputString[:-1]

#para cada artigo no DOU
for article in root:

    #Gerando um objeto artigo vazio
    local_artigo = Artigo()

    #Para cada atributo existente, sobrescreva o atributo local inicialmente vazio
    for atributo in article.attrib:
        setattr( local_artigo, atributo, article.attrib[atributo].encode('utf-8').strip() )

    #Pegando cada uma das 5 tags dentro do corpo
    for body in article:
        for child in body:
            try:
                setattr( local_artigo, child.tag, child.text.encode('utf-8').strip() )
            except AttributeError:
                setattr( local_artigo, child.tag, 'null' )
            
            if child.tag == 'Autores':
                local_artigo.Autores = ''
                for grandchild in child:
                    try:
                        local_artigo.Autores += "<"+grandchild.tag.encode('utf-8')+"><"+grandchild.text.encode('utf-8')+"></"+grandchild.tag.encode('utf-8')+">"
                    except AttributeError:
                        local_artigo.Autores += "<"+grandchild.tag.encode('utf-8')+"></"+grandchild.tag.encode('utf-8')+">"
                if local_artigo.Autores == '':
                    local_artigo.Autores = 'null'

            if child.tag == 'Texto':
                local_artigo.qtdParagrafos = str(len( RegexSub('<p[^>]*', '', child.text.encode('utf-8')).split('</p>'))).strip()
                local_artigo.qtdTermos = str(len( RegexFindAll('(NOMEAR)|(DISPENSAR)|(EXONERAR)|(DESLIGAR)|([^N]CEDER)|(DEMITIR)', NORM(child.text.encode('utf-8')).upper()))).strip()


    #iterando sobre os atributos do objeto para construir a saida para o arquivo txt
    outputString=""
    for item in listaAttributos:
        outputString += getattr(local_artigo, item) + '\t'

    #lembrando de ignorar o último tab
    print outputString[:-1]

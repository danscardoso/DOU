# -*- coding: utf-8 -*-

from sys import argv
import xml.etree.ElementTree as ET #library to read xml in python, structure-comprehensible

#recebe o nome do arquivo via CLI
nome_arquivo = argv[1];

class Artigo:
    id='null'
    artType='null'          #ato
    pubDate='null'          #data
    artCategory='null'      #orgao
    name='null'
    idOficio='null'
    pubName='null'
    artClass='null'
    artSection='null'
    artSize='null'
    artNotes='null'
    numberPage='null'
    pdfPage='null'
    editionNumber='null'
    Identifica='null'
    Data='null'
    Ementa='null'
    Titulo='null'
    SubTitulo='null'
    Texto='null'

print ("id\tato\tdata\torgao\tname\tidOficio\tpubName\tartClass\tartSection\tartSize\tartNotes\tnumberPage\tpdfPage\teditionNumber\tIdentifica\tData\tEmenta\tTitulo\tSubtitulo\tTexto")

#root is XML tag
tree = ET.parse(nome_arquivo)
root = tree.getroot()           #xml tag

local_artigo = Artigo()
listaAttributos = [a for a in dir(local_artigo) if not a.startswith('__') and not callable(getattr(local_artigo,a))]

#para cada artigo no DOU
for article in root:

    #Gerando um objeto artigo vazio
    local_artigo = Artigo()

    #Para cada atributo existente, sobrescreva o atributo local inicialmente vazio
    for atributo in article.attrib:
        setattr( local_artigo, atributo, article.attrib[atributo].encode('utf-8') )

    #Pegando cada uma das 5 tags dentro do corpo
    for body in article:
        for child in body:
            try:
                setattr( local_artigo, child.tag, child.text.encode('utf-8') )
            except AttributeError:
                setattr( local_artigo, child.tag, 'null' )

    #iterando sobre os atributos do objeto para construir a saida para o arquivo txt
    outputString=""
    for item in listaAttributos:
        outputString += getattr(local_artigo, item) + '\t'

    #lembrando de ignorar o último tab
    print outputString[:-1]


    #print ( local_artigo.id + '\t' +
    #        local_artigo.artType + '\t' +
    #        local_artigo.pubDate + '\t' +
    #        local_artigo.artCategory + '\t' +
    #        local_artigo.name + '\t' +
    #        local_artigo.idOficio + '\t' +
    #        local_artigo.pubName + '\t' +
    #        local_artigo.artClass + '\t' +
    #        local_artigo.artSection + '\t' +
    #        local_artigo.artSize + '\t' +
    #        local_artigo.artNotes + '\t' +
    #        local_artigo.numberPage + '\t' +
    #        local_artigo.pdfPage + '\t' +
    #        local_artigo.editionNumber + '\t' +
    #        local_artigo.Identifica + '\t' +
    #        local_artigo.Data + '\t' +
    #        local_artigo.Ementa + '\t' +
    #        local_artigo.Titulo + '\t' +
    #        local_artigo.SubTitulo + '\t' +
    #        local_artigo.Texto)

# -*- coding: utf-8 -*-
# DATA FROM THE SECTIONS 2 AND 3 OF THE DOU (OFFICIAL DIARY OF THE UNION) AVAILABLE AT: http://dados.gov.br/organization/imprensa-nacional-in SINCE DEC/17
import re
from sys import argv as CLI_input

class objetoSaida:
    idArtigo='null'
    ato='null'
    orgao='null'
    data='null'
    main_orgao='null'
    mesAno='null'
    verbo='null'
    nome='null'
    cargo='null'
    linha='null'
    qtdParagrafos='null'
    qtdTermos='null'
    texto='null'

def print_cabecalho_output():
    outputString = ''
    for atributo in listaAttributos:
        outputString += atributo + "\t"
    print outputString[:-1]

def print_registro( registro ):
    outputString = ''
    
    for atributo in listaAttributos:
        outputString += str(getattr( registro,atributo)) + "\t"
    print outputString[:-1]

#function to remove strange characters and accents
def NORM(nome):
    nome=re.sub('Á|À|Â|Ä|Ã','A',nome)
    nome=re.sub('á|à|â|ä|ã','a',nome)
    nome=re.sub('É|È|Ê|Ë','E',nome)
    nome=re.sub('é|è|ê|ë','e',nome)
    nome=re.sub('Í|Ì|Î|Ï','I',nome)
    nome=re.sub('í|ì|î|ï','i',nome)
    nome=re.sub('Ó|Ò|Ô|Ö|Õ','O',nome)
    nome=re.sub('ó|ò|ô|ö|õ','o',nome)
    nome=re.sub('Ú|Ù|Û|Ü','U',nome)
    nome=re.sub('ú|ù|û|ü','u',nome)
    nome=re.sub("\'|\"|\*|\\|ª|º|º",' ',nome)
    nome=nome.replace('ç','c')
    nome=nome.replace('Ç','C')
    nome=nome.replace('ñ','n')
    nome=nome.replace('Ñ','N')
    return str(nome)

#recebe o nome do arquivo via CLI
nome_arquivo = CLI_input[1];

#verbs used as flags to identify desirable information, terms of importance
termos = ['NOMEAR','DISPENSAR','EXONERAR','DESLIGAR',' CEDER','DEMITIR']

#lista de atributos para saida
temp = objetoSaida()
listaAttributos = [a for a in dir(temp) if not a.startswith('__') and not callable(getattr(temp,a))]

#Print cabecalho
print_cabecalho_output()

with open(nome_arquivo) as input_file:

    #cabecalho eh um caso a parte
    cabecalho = input_file.readline().strip().split('\t')

    #registro a registro
    for registro in input_file:

        registro = registro.split('\t')

        output = objetoSaida()
        output.ato           = registro[ cabecalho.index('artType') ]
        output.data          = registro[ cabecalho.index('pubDate') ]
        output.idArtigo      = registro[ cabecalho.index('id') ]
        output.orgao         = registro[ cabecalho.index('artCategory') ]
        output.main_orgao    =  registro[ cabecalho.index('artSection') ]
        output.texto         = registro[ cabecalho.index('Texto') ]
        output.qtdParagrafos = registro[ cabecalho.index('qtdParagrafos') ]

        #Mesano eh a data ignorando o dia
        output.mesAno     = output.data[3:].replace('/','')

        #Texto Trabalhado
        textoTrabalhado = NORM(output.texto)

        #Quebrando o texto em uma lista de paragrafos
        paragrafos = re.sub('<p[^>]*', '', textoTrabalhado).split('</p>')

        #Quantidade de termos
        
        #output.verbo      = registro[ cabecalho.index('artCategory') ]
        #output.nome       = registro[ cabecalho.index('artCategory') ]
        #output.cargo      = registro[ cabecalho.index('artCategory') ]
        #output.linha      = registro[ cabecalho.index('artCategory') ]
    
        print_registro( output )

# -*- coding: utf-8 -*-
from sys import argv
import re

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

class Artigo:
    
    idArtigo='null'
    ato='null'
    dataArtigo='null'
    dataPublicacao='null'
    mesAnoPub='null'
    orgao='null'
    main_orgao='null'
    texto='null'

    #Informações novas
    qtdParagrafos='null'
    qtdTermos='null'
    interesse='null'
    listaTermos='null'

#recebe o nome do arquivo via CLI
nome_arquivo = argv[1];

local_artigo = Artigo()
listaAttributos = [a for a in dir(local_artigo) if not a.startswith('__') and not callable(getattr(local_artigo,a))]

#Imprimindo o cabecalho
print_cabecalho_output()

with open(nome_arquivo) as input_file:

    #cabecalho eh um caso a parte
    cabecalho = input_file.readline().split('\t')

    #registro a registro
    for registro in input_file:

        registro = registro.split('\t')

        a = Artigo()
        a.ato            = registro[ cabecalho.index('artType') ]
        a.dataPublicacao = registro[ cabecalho.index('pubDate') ]
        a.idArtigo       = registro[ cabecalho.index('id') ]
        a.orgao          = registro[ cabecalho.index('artCategory') ]
        a.main_orgao     = registro[ cabecalho.index('artSection') ]
        a.texto          = re.sub(' +', ' ', registro[ cabecalho.index('Texto') ])

        #MesAno eh a data ignorando o dia
        a.mesAnoPub = a.dataPublicacao[3:].replace('/','')

        #Trabalhando melhor a data
        dataArtigo = NORM(registro[ cabecalho.index('Data') ]).upper()
        a.dataArtigo = re.sub('^[^0-9]+', '', re.sub('\.$', '', dataArtigo).replace('.', '/')).replace(' DE ', '/').replace('JANEIRO', '01').replace('FEVEREIRO', '02').replace('MARCO','03').replace('ABRIL','04').replace('MAIO','05').replace('JUNHO','06').replace('JULHO','07').replace('AGOSTO','08').replace('SETEMBRO','09').replace('OUTUBRO','10').replace('NOVEMBRO','11').replace('DEZEMBRO','12').replace(' ', '')

        #Texto Trabalhado
        textoTrabalhado = NORM(a.texto)

        #Quebrando o texto em uma lista de paragrafos
        paragrafos = re.sub('<p[^>]*', '', textoTrabalhado).split('</p>')

        #Quantidade de termos
        a.qtdParagrafos = str(len(paragrafos)).strip()
        
        pesquisaTermos = re.findall('(NOMEAR)|(DISPENSAR)|(EXONERAR)|(DESLIGAR)|([^\w]CEDER)|(DEMITIR)', textoTrabalhado.upper())

        if pesquisaTermos:
            a.listaTermos=''

            #não me pergunte por que mas o regex volta em grupos de matches
            for grupo in pesquisaTermos:
                for item in grupo:
                    if item != '':
                        a.listaTermos += str(re.sub( '\W', '', item)) + "," 

            #ignorando a ultima virgula
            a.listaTermos = a.listaTermos[:-1]

        #quantidade de termos
        a.qtdTermos = str(len( pesquisaTermos )).strip()
        


        #Definindo se é de interesse ou não
        a.interesse = a.qtdTermos > 0

        print_registro( a )

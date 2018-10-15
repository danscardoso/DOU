# -*- coding: utf-8 -*-
from sys import argv
import re

#TODO: QUEBRAR ARTIGOS COM MAIS DE UM OBJETO, TEXTO, ASSINA E MAIS TEXTO
# EM ARTIGOS QUE TERMINAM NA ASSINATURA (CASO ELA EXISTA)

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
    
    #Informações mantidas
    ato='null'
    dataPublicacao='null'
    orgao='null'
    main_orgao='null'
    texto='null'

    #Informações editadas para "melhorar" um pouco
    dataArtigo='null'
    referencia='null'           # link para acessar o documento original no site da imprensa


    #Informações que vem do xml que eu ignorei e não passei adiante
    ### artClass='null'
    ### artNotes='null'
    ### artSize='null'
    ### editionNumber='null'
    ### highlight='null'
    ### highlightPriority='null'
    ### highlightType='null'
    ### id='null'
    ### idMateria='null'
    ### idOficio='null'
    ### name='null'
    ### numberPage='null'
    ### pubName='null'
    ### Autores='null'
    ### Data='null'
    ### Ementa='null'
    ### Identifica='null'
    ### SubTitulo='null'
    ### Titulo='null'

    #Informações novas
    qtdParagrafos='null'        # quantidade de tags <p> no texto
    qtdTermos='null'            # quantidade de termos de interesse (aqueles verbos)
    interesse='null'            # binário, avalia se qtdTermos > 0
    listaTermos='null'          # os termos de interesse separados por ,
    orgaoCodigo='null'          # 
    mesAnoPub='null'            # mesAno da publicação para facilitar paginação



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

        reg = Artigo()
        reg.ato            = registro[ cabecalho.index('artType') ]
        reg.dataPublicacao = registro[ cabecalho.index('pubDate') ]
        reg.orgao          = registro[ cabecalho.index('artCategory') ]
        reg.main_orgao     = registro[ cabecalho.index('artSection') ]
        reg.texto          = re.sub(' +', ' ', registro[ cabecalho.index('Texto') ])

        #MesAno eh a data ignorando o dia
        reg.mesAnoPub = reg.dataPublicacao[3:].replace('/','')

        #Trabalhando melhor a data
        dataArtigo = NORM(registro[ cabecalho.index('Data') ]).upper()
        reg.dataArtigo = re.sub('^[^0-9]+', '', re.sub('\.$', '', dataArtigo).replace('.', '/')).replace(' DE ', '/').replace('JANEIRO', '01').replace('FEVEREIRO', '02').replace('MARCO','03').replace('ABRIL','04').replace('MAIO','05').replace('JUNHO','06').replace('JULHO','07').replace('AGOSTO','08').replace('SETEMBRO','09').replace('OUTUBRO','10').replace('NOVEMBRO','11').replace('DEZEMBRO','12').replace(' ', '')

        #Pega o código numérico que vem no xml (12 códigos seguidos, separados por : cada um com 10k possibilidades)
        niveis = registro[ cabecalho.index('artClass') ].split(':')
        reg.orgaoCodigo = niveis[0]


        #Ajustando a referência ao original
        reg.referencia = registro[ cabecalho.index('pdfPage') ].replace('amp;', '').replace('[amp]', '&')

        #Texto Trabalhado
        textoTrabalhado = NORM(reg.texto)

        #Quebrando o texto em uma lista de paragrafos
        paragrafos = re.sub('<p[^>]*', '', textoTrabalhado).split('</p>')

        #Quantidade de termos
        reg.qtdParagrafos = str(len(paragrafos) -1).strip()
        
        pesquisaTermos = re.findall('(NOMEAR)|(DISPENSAR)|(EXONERAR)|(DESLIGAR)|([^\w]CEDER)|(DEMITIR)', textoTrabalhado.upper())

        if pesquisaTermos:
            reg.listaTermos=''

            #não me pergunte por que mas o regex volta em grupos de matches
            # por conta disso, tem que passar de grupo em grupo juntando de novo para
            # transformar em uma lista de novo
            for grupo in pesquisaTermos:
                for item in grupo:
                    if item != '':
                        reg.listaTermos += str(re.sub( '\W', '', item)) + "," 

            #ignorando a ultima virgula
            reg.listaTermos = reg.listaTermos[:-1]

        #quantidade de termos
        reg.qtdTermos = str(len( pesquisaTermos )).strip()
        
        #Definindo se é de interesse ou não
        reg.interesse = int(reg.qtdTermos) > 0

        print_registro( reg )

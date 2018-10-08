# -*- coding: utf-8 -*-
# DATA FROM THE SECTIONS 2 AND 3 OF THE DOU (OFFICIAL DIARY OF THE UNION) AVAILABLE AT: http://dados.gov.br/organization/imprensa-nacional-in SINCE DEC/17
import re
from sys import argv as CLI_input

class Acao:

    # Atributos vindo do artigo
    idArtigo='null'
    ato='null'
    #dataArtigo='null'
    dataPublicacao='null'
    mesAnoPub='null'
    orgao='null'
    main_orgao='null'
    #texto='null'
    qtdParagrafos='null'
    qtdTermos='null'
    #interesse='null'
    #listaTermos='null'

    #Variaveis locais da acao
    preambulo='null'
    verbo='null'
    nome='null'
    cargo='null'
    textoAcao='null'

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

def isnome(termo):

    #Blacklist de termos que não podem
    vet_black = ['SR.', 'SR', '-', 'CPF', 'SIAPE', 'CRP', 'DOU'] + termos

    # Vai dar match de algo que não seja uma letra, aspas simple, dupla, traço ou ponto
    # Daí inverte (se achar algo suspeito, retorna falso)
    if re.search('^[^A-Z\'\-\.\,"]+$', termo):
        print (termo + " reprovado pelo regex")
        return False
    return True

#recebe o nome do arquivo via CLI
nome_arquivo = CLI_input[1];

#lista de atributos para saida
temp = Acao()
listaAttributos = [a for a in dir(temp) if not a.startswith('__') and not callable(getattr(temp,a))]

#Print cabecalho
print_cabecalho_output()

with open(nome_arquivo) as input_file:

    #cabecalho eh um caso a parte
    cabecalho = input_file.readline().strip().split('\t')

    #registro a registro
    for registro in input_file:

        registro = registro.split('\t')

        a = Acao()
        a.idArtigo       = registro[ cabecalho.index('idArtigo') ]
        a.ato            = registro[ cabecalho.index('ato') ]
        a.dataPublicacao = registro[ cabecalho.index('dataPublicacao') ]
        a.mesAnoPub      = registro[ cabecalho.index('mesAnoPub') ]
        a.orgao          = registro[ cabecalho.index('orgao') ]
        a.main_orgao     = registro[ cabecalho.index('main_orgao') ]
        a.qtdParagrafos  = registro[ cabecalho.index('qtdParagrafos') ]
        a.qtdTermos      = registro[ cabecalho.index('qtdTermos') ]
        
        textoTrabalhado = NORM(registro[ cabecalho.index('texto') ].strip())

        #Lista de termos
        listaTermos = registro[ cabecalho.index('listaTermos') ].split(",")

        #Lista de verbos de interesse (em forma de regex)
        termos = ['NOMEAR','DISPENSAR','EXONERAR','DESLIGAR','[^\w]CEDER','DEMITIR']
        
        #Quebrando o texto nos verbos de interesse
        if int(a.qtdTermos):
            
            #Em um primeiro momento eh uma "partição" de uma parte
            textoParticionado = [textoTrabalhado]

            for termo in termos:
                temp=[]
                for pedaco in textoParticionado:
                    temp += re.split(termo, pedaco, flags=re.IGNORECASE)
                textoParticionado = temp

            #Tiro o preambulo da lista de ações
            a.preambulo = textoParticionado.pop(0)

            #Se o preambulo ajudar, procura o orgao
            if a.preambulo.find('class= titulo') != -1:
                a.orgao = re.search("class= titulo >[^<]+", a.preambulo).group(0)[15:]

            # Para cada açao restante
            for index, acao in enumerate(textoParticionado):
                a.textoAcao = listaTermos[index] + acao
                a.verbo = listaTermos[index]

                #busca nome
                palavras = acao.split(' ')
                for id, palavra in enumerate(palavras):

                    # Se tiver 2 válidos em sequencia
                    if isnome( palavras[id] ) and isnome( palavras[id+1] ):
                        nome_ini = id
                        break

                for id,palavra in enumerate(palavras[nome_ini:]):
                    if palavra.find(',') != -1:
                        nome_fim = id+1
                        break
                    elif not isnome( palavra ):
                        nome_fim = id
                        break

                a.nome = (' '.join(c for c in palavras[nome_ini:(nome_ini+nome_fim)])).replace(',','')

                #cargo
                if acao.find('compor o ') != -1 :
                    a.cargo = re.search("compor o [^,.]+", acao).group(0)[9:]
                elif acao.find('cargo de') != -1 :
                    a.cargo = re.search("cargo de [^,.]+", acao).group(0)[9:]
                elif acao.find('funcao de') != -1:
                    a.cargo = re.search("funcao de [^,.]+", acao).group(0)[10:]

                print_registro( a )
        else:
            print_registro( a )


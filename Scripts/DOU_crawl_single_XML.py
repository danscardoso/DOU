# -*- coding: utf-8 -*-
# DATA FROM THE SECTIONS 2 AND 3 OF THE DOU (OFFICIAL DIARY OF THE UNION) AVAILABLE AT: http://dados.gov.br/organization/imprensa-nacional-in SINCE DEC/17
import glob, os, time, re, sys
from unicodedata import normalize
import xml.etree.ElementTree as ET #library to read xml in python, structure-comprehensible

#recebe o nome od arquivo via CLI
nome_arquivo = sys.argv[1];

def isnome(termo):
    termo = termo.upper()
    vet_white = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',"'",'-','.','"']
    vet_black = ['SR.', 'SR', '-', 'CPF', 'SIAPE', 'CRP', 'DOU'] + termos
    if termo in vet_black:
        return False
    for char in termo:
        if char not in vet_white:
            return False
    return True


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

#verbs used as flags to identify desirable information, terms of importance
termos = ['NOMEAR','DISPENSAR','EXONERAR','DESLIGAR',' CEDER','DEMITIR']

#arq_saida = open('RESULTADO_TERMOS_20180726.txt','w',0) #output
print ("article_id\tato\tmain_orgao\torgao\tdata\tverbo\tnome\tlinha")

tree = ET.parse(nome_arquivo)

#root is XML tag
root = tree.getroot()           #xml tag

#para cada artigo no DOU
for article in root:

    article_id = article.attrib['id']
    orgao = article.attrib['artCategory'] #gathering the organization

    main_orgao = re.search('^[^/]+',orgao).group(0)

    data = article.attrib['pubDate'] #gathering publication date
    ato = article.attrib['artType'] #gathering the type of article     


    ############# Padrão 1 - Decreto de pessoal
    if ato == 'Decreto de Pessoal':

        for texto in article.iter('Texto'):

            paragrafos = NORM(texto.text.encode('utf-8')).replace('</p>' ,'').split('<p>')

            verbo_encontrado='';
            for id, paragrafo in enumerate(paragrafos):

                #Se encontrar o verbo em um parágrafo, no seguinte pegue o nome
                if verbo_encontrado == True:

                    palavras = paragrafo.split(' ')
                    for id, palavra in enumerate(palavras):

                        if isnome ( unicode(palavra, 'utf-8')) and palavra == palavra.upper() and palavras[id+1] == palavras[id+1].upper():
                            nome_ini = id
                            break

                    for id,palavra in enumerate(palavras[nome_ini:]):
                        if palavra.find(',') != -1:
                            nome_fim = id+1
                            break
                        else:
                            if palavra != palavra.upper() or isnome(palavra) == False:
                                nome_fim = id
                                break                            
                    nome = (' '.join(c for c in palavras[nome_ini:(nome_ini+nome_fim)])).replace(',','')

                    #nome = re.search('[A-Z ]+', NORM(paragrafo)).group(0)
                    print (article_id+'\t'+ato.encode('utf-8')+'\t'+main_orgao.encode('utf-8')+'\t'+orgao.encode('utf-8')+'\t'+data+'\t'+verbo+'\t'+nome+'\t'+paragrafo) #output
                    break

                for termo in termos: #identifying if there is any term of importance within the text
                    pos_termo = paragrafo.find(termo)
                    if pos_termo != -1:
                        verbo = termo
                        verbo_encontrado = True
                        break
                

    ############# Padrão 2 - Caso Geral
    else:
        for texto in article.iter('Texto'):
            
            texto = texto.text.encode('utf-8').replace('</p>','')
            
            paragrafos = NORM(texto).split('<p>')
            for paragrafo in paragrafos:
                line_temp = paragrafo.upper()
                pos_termo = -1
                
                for termo in termos:
                    pos_termo = line_temp.find(termo)
                    if pos_termo != -1:
                        verbo = termo
                        break

                if pos_termo == -1:
                    continue
                    
                #gathering the NAME OF THE INDIVIDUAL. Note: struggling now with the various forms a name can appear. (upper/lower case, titles, and so on)
                try:
                    linha_temp = paragrafo[pos_termo:].split(' ')
                    nome_ini = -1
                    nome_fim = -1

                    for id,palavra in enumerate(linha_temp):
                        
                        if isnome ( unicode(palavra, 'utf-8')) and palavra == palavra.upper() and linha_temp[id+1] == linha_temp[id+1].upper():
                            nome_ini = id
                            break

                    for id,palavra in enumerate(linha_temp[nome_ini:]):
                        if palavra.find(',') != -1:
                            nome_fim = id+1
                            break
                        else:
                            if palavra != palavra.upper() or isnome(palavra) == False:
                                nome_fim = id
                                break                            
                    nome = (' '.join(c for c in linha_temp[nome_ini:(nome_ini+nome_fim)])).replace(',','')
                except:
                    nome = ''
                    
                print (article_id+'\t'+ato.encode('utf-8')+'\t'+main_orgao.encode('utf-8')+'\t'+orgao.encode('utf-8')+'\t'+data+'\t'+verbo+'\t'+nome+'\t'+paragrafo) #output
                #arq_saida.write(temp+'\n')

#arq_saida.close()

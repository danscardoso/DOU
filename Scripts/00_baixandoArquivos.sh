#! /bin/bash

# A ideia eh que input eh um dos seguintes valores:
#	"1"
#	"2"
#	"3"
#	"1,2"
#	"1,3"
#	"2,3"
#	"1,2,3"
binSecao1=$(echo $1 | grep -o "1")
binSecao2=$(echo $1 | grep -o "2")
binSecao3=$(echo $1 | grep -o "3")
# Se o usuário pedir os greps dão match e as variaveis passam a ter o valor binárias dão match, se não pedir ficam vazias

if [ -z $1 ]; then
	echo "Informe qual seção deve ser (1, 2 ou 3 ou uma combinação delas)"
	exit
fi

# Arquivos usados pelo programa
temporary_file="__temp.txt"
temporary_file2="__temp2.txt"
log_file="__log.txt"

#Apagando o log caso tenha persistido
if [ -f $log_file ];then
	rm $log_file
fi

#Eles separam os dados em paginas para cada ano
for ano in {2002..2018}; do

	# Primeiro vamos pegar a URL base por ano e colocar no arquivo, caso
	# diferente para a url de 2017
	if [ $ano -eq '2017' ];then
		urlTronco="http://dados.gov.br/dataset/diario-oficial-da-uniao"
	else
		urlTronco="http://dados.gov.br/dataset/diario-oficial-da-uniao-materias-publicadas-em-"$ano
	fi
	
	# Pega a url, bota no arquivo temporario1 e loga
	echo "[ano="$ano"] [URL tronco]" $urlTronco >> $log_file
	wget $urlTronco --timeout=10 -t0 -O $temporary_file

	# Dentro da página de cada ano (salva no arquivo temporario), eles tem n
	# arquivos pois eles separam por seção e por mês (até 3 seções e 12 meses
	# por ano)

	# cada match do grep eh um recurso a ser baixado
	for recurso in $( grep -o -E 'a class="heading"[^>]+' $temporary_file | tr -d " "); do

		#Puxando a url do recurso
		urlGalho="http://dados.gov.br/"$( echo $recurso | grep -o -E "dataset[^\"]*" )

		#Puxando a seção do recurso
		secao=$( echo $recurso | grep -o -E "Seção[0-9]" | grep -o -E "[0-9]" )

		# Se o usuário pedir a seção no começo e o recurso for da seção pedida
		if ( ! [ -z $binSecao1 ] && [ $secao = $binSecao1 ] ) || ( ! [ -z $binSecao2 ] && [ $secao = $binSecao2 ] ) || ( ! [ -z $binSecao3 ] && [ $secao = $binSecao3 ] ); then
			wget $urlGalho --timeout=10 -t0 -O $temporary_file2
			echo "[ano="$ano"] [URL galho] " $urlGalho >> $log_file
		
			#Descobrindo a URL do recurso final
			saida=$( grep -o -E "muted ellipsis\">[^>]*" $temporary_file2 | grep -o 'href="[^"]*' | grep -o "http.*" )

			#Pegando o nome do arquivo zip para nomear o arquivo de saida
			nome_saida=$( echo $saida | grep -E -o -i "/[0-9A-Z\.]+/[a-z0-9\-]+$" | grep -E -o -i "^/[a-z0-9]+" | grep -o -i -E "[a-z0-9]+")

			#Pegando e logando qual recurso eu estou tentado buscar:
			wget $saida --timeout=10 -t0 -O "../dados_originais/"$nome_saida".zip"
			echo "[ano="$ano"] [URL folha] ["$nome_saida"] "$saida >> $log_file
		else
			echo "[ano="$ano"] [URL galho ignorado] " $urlGalho >> $log_file
		fi

	done
done

#rm $temporary_file $temporary_file2

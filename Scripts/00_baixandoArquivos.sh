#! /bin/bash

#
temporary_file="__temp.txt"
temporary_file2="__temp2.txt"
log_file="__log.txt"

#Apagando o log caso tenha persistido
if [ -f $log_file ];then
	rm $log_file
fi

#Eles separam os dados em paginas para cada ano
for ano in {2002..2018}; do

	# Caso separado para a url de 2017
	if [ $ano -eq '2017' ];then
		wget "http://dados.gov.br/dataset/diario-oficial-da-uniao" --timeout=10 -t0 -O $temporary_file
	else
		wget "http://dados.gov.br/dataset/diario-oficial-da-uniao-materias-publicadas-em-"$ano --timeout=10 -t0 -O $temporary_file
	fi

	#Logando qual URL tronco eu estou tentando buscar
	echo "[ano="$ano"] [URL tronco] http://dados.gov.br/dataset/diario-oficial-da-uniao-materias-publicadas-em-"$ano >> $log_file

	#Dentro da página de cada ano (salva no arquivo temporario), eles tem n arquivos pois eles separam por seção e por mês
	# (até 3 seções e 12 meses por ano)
	#
	# cada match do grep eh um recurso a ser baixado
	for recurso in $( grep -o 'a class="heading" href="[^"]*' $temporary_file | grep -o "dataset.*" ); do

		#Logando qual URL eu estou tentando buscar
		echo "[ano="$ano"] [URL galho] http://dados.gov.br/"$recurso >> $log_file
		
		wget "http://dados.gov.br/"$recurso --timeout=10 -t0 -O $temporary_file2

		saida=$( grep -o "muted ellipsis\">[^>]*" $temporary_file2 | grep -o 'href="[^"]*' | grep -o "http.*" )

		nome_saida=$( echo $saida | grep -E -o -i "/[0-9A-Z\.]+/[a-z0-9\-]+$" | grep -E -o -i "^/[a-z0-9]+" | grep -o -i -E "[a-z0-9]+")

		#Logando qual recurso eu estou tentado buscar:
		echo "[ano="$ano"] [URL folha] ["$nome_saida"] "$saida >> $log_file

		wget $saida --timeout=10 -t0 -O "../dados_originais/"$nome_saida".zip"

	done
done

#rm $temporary_file $temporary_file2


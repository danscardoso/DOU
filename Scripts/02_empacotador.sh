# !bin/bash
#
# Empacota um diretorio cheio de arquivos XML em um arquivo xml soh
#
# Usage: ./empacotador.sh diretorio arquivo_output
#
# Exemplo:
# ./empacotador.sh ../dados_unzip ../empacotados.xml
#

diretorio=$1
nome_arquivo_temp="__temp.out"
nome_arquivo_output=$2

# TODO: CHECAR SE ELE VAI CUSPIR SEM OS ENDINGS DO WINDOWS (\r\n)

echo "COMECEI O EMPACOTAMENTO" $(date +"%T")

# CONCATENAÇÃO DOS ARQUIVOS FONTE
find "$diretorio" -name "*.xml" | xargs -d '\n' cat > $nome_arquivo_temp

# OPERAÇÕES PARA AJUSTAR O ARQUIVO RESULTANTE
#	# primeiro sed: retira as tags xml e strong
#	# segundo sed: remove os paragrafos vazios
#	# terceiro e quarto sed: remove espaços desnecessários ao abrir e fechar tags
#	# quinto sed: adiciona na primeira linha a tag xml
#	# echo: adiciona o fechamento da tag xml no final do documento
sed -E 's/<(\/?xml>)|(<\/?strong>)//g' $nome_arquivo_temp | sed -E 's/<p>[ .]*<\/p>//g' | sed -E 's/ +</</g' | sed -E 's/> +/>/g' | sed 's/&//g' | sed '1s/^/<xml>/' | sed 's/\r//' > "$nome_arquivo_output"
echo '</xml>' >> "$nome_arquivo_output"

rm $nome_arquivo_temp

echo "TERMINEI O EMPACOTAMENTO" $(date +"%T")

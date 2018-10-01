# 1 - PREPARAÇÃO DE TODO O AMBIENTE
# 	* REQUISITO UMA PASTA FONTE COM ARQUIVOS ZIPADOS
#	* REQUISITO UM NOME PARA UMA PASTA PARA GUARDAR OS ARQUIVOS UNZIPADOS

# exemplo:
# ./01_prepara_ambiente.sh ../dados_originais ../dados_unzip
#

echo "COMECEI A PREPARAR O AMBIENTE" $(date +"%T")

source_file_dir=$1
unzipped_file_dir=$2
caminho_relativo=$( echo $0 | sed 's/01_prepara_ambiente.sh$//' | sed 's/^\.\///' )

#Faz uma pasta para conter os arquivos unzipados
mkdir -p "$unzipped_file_dir"

#unzipa tudo na pasta dados_originais
IFS=$'\n'
for file in $(find "$source_file_dir" -name "*zip"); do

	#pasta eh o arquivo zip sem o caminho relativo e sem o .zip
	folder=$(echo $file | grep -E -o '[^/]*$' | sed 's/\.zip//' )

	#unzipa lah
	unzip -q "$file" -d "$unzipped_file_dir""/""$folder"
done

"./"$caminho_relativo"empacotador.sh" $unzipped_file_dir "../empacotados.xml"

echo "TERMINEI DE PREPARAR O AMBIENTE" $(date +"%T")

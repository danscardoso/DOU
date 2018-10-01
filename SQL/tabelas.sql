CREATE SCHEMA DOU 

DROP TABLE DOU.ARTIGOS CASCADE;

--CREATE TABLE DOU.ARTIGOS (
--	article_id bigserial primary key,
--	ato text,
--	data date,
--	orgao text,
--	art_name varchar(32),
--	art_idOficio numeric(7,0),
--	art_pubName varchar(72),
--	art_artClass text,
--	art_artSection text,
--	art_artSize numeric(2,0),
--	art_artNotes text,
--	art_numberPage text,
--	art_pdfPage text,
--	art_editionNumber varchar(6),
--	art_texto text
--);

CREATE TABLE DOU.ARTIGOS (
	article_id text,
	ato text,
	data date,
	orgao text,
	art_name text,
	art_idOficio text,
	art_pubName text,
	art_artClass text,
	art_artSection text,
	art_artSize text,
	art_artNotes text,
	art_numberPage text,
	art_pdfPage text,
	art_editionNumber text,
	art_texto text
);

---------------------
\COPY DOU.ARTIGOS FROM 'C:/Users/pedro.palotti/Downloads/DOU/Outputs/dados_banco_relacional_sem_cabecalho.txt' ( FORMAT('text'), DELIMITER(E'\t') )

truncate dou.artigos;

select * from dou.artigos limit 1
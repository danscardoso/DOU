SELECT
	article_id
	,artigos.data
	,char_length(artigos.art_texto) as qtd_caracteres
	,art_texto
FROM dou.artigos
where
	art_texto  ~ '.*DECRETO DE.*' AND
	art_texto !~ '.*DECRETOS DE.*'
order by 1

SELECT
	article_id
FROM dou.artigos

select regexp_replace(
			regexp_replace(
				regexp_replace(art_name, '^RET-', ''), 
			'((-SEC2.*)|(-S-2)|(-S2))$', ''),
		'^[a-z0-9\-]*DEP\-?', ''), art_name
from dou.ARTIGOS
where ato = 'Decreto de Pessoal'
order by 1


select article_id, count(*) as contagem
from dou.artigos
group by 1
order by contagem,1

select * 
from dou.artigos
where ato = 'Decreto de Pessoal'
order by data


select *
from dou.artigos
where ato = ''
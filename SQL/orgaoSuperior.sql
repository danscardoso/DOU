select
	count(*) as contagem
	,regexp_replace(orgao, '/.*', '') as orgaoSupCalculado
	,orgao as orgaoInformado
from dou.artigos
group by orgao
order by contagem desc, 1;


select
	count(*) as contagem
	,regexp_replace(orgao, '/.*', '') as orgaoSupCalculado
--	,orgao as orgaoInformado
from dou.artigos
group by orgaoSupCalculado
order by contagem desc, 1;
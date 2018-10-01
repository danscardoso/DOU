select ato, count(*)
from dou.artigos
group by 1
order by 2 desc, 1
select avg(10*score + 15*is_accepted::integer)::real
from answer
where created_at >= current_date - 30

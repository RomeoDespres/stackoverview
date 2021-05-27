select
    tag_id as tag,
    avg(10*answer.score + 15*answer.is_accepted::integer)::real as reputation
from
    answer
    join question on question.id = answer.question_id
    join question_tag on question.id = question_tag.question_id
where
    answer.score between -1 and 10
    and answer.created_at >= current_date - 30
group by tag_id
having count(*) > 100
order by 2 desc
limit %(limit)s
offset %(offset)s

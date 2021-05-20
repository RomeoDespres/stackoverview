delete from question_tag where question_id in %s;
insert into question_tag (question_id, tag_id)
    values (%(question_id)s, %(tag_id)s)

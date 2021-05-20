insert into answer (
    id,
    question_id,
    is_accepted,
    created_at,
    score,
    last_active_at,
    account_id
)
    values (
        %(answer_id)s,
        %(question_id)s,
        %(is_accepted)s,
        to_timestamp(%(creation_date)s),
        %(score)s,
        to_timestamp(%(last_activity_date)s),
        %(owner_id)s
    )
    on conflict (id) do update set
        is_accepted=%(is_accepted)s,
        created_at=to_timestamp(%(creation_date)s),
        score=%(score)s,
        last_active_at=to_timestamp(%(last_activity_date)s),
        account_id=%(owner_id)s

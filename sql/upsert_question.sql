insert into question (
    id,
    created_at,
    score,
    last_active_at,
    views,
    link,
    title,
    account_id
)
    values (
        %(question_id)s,
        to_timestamp(%(creation_date)s),
        %(score)s,
        to_timestamp(%(last_activity_date)s),
        %(view_count)s,
        %(link)s,
        %(title)s,
        %(owner_id)s
    )
    on conflict (id) do update set
        created_at=to_timestamp(%(creation_date)s),
        score=%(score)s,
        last_active_at=to_timestamp(%(last_activity_date)s),
        views=%(view_count)s,
        link=%(link)s,
        title=%(title)s,
        account_id=%(owner_id)s

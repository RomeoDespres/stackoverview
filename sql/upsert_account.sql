insert into account (id, type, profile_image_link, name, link)
    values (
        %(user_id)s,
        %(user_type)s,
        %(profile_image)s,
        %(display_name)s,
        %(link)s
    )
    on conflict (id) do update set
        type = %(user_type)s,
        profile_image_link = %(profile_image)s,
        name = %(display_name)s,
        link = %(link)s

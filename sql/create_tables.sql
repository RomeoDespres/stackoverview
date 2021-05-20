create table account (
  id integer primary key,
  type text not null,
  profile_image_link text not null,
  name text not null,
  link text
);


create table question (
  id integer primary key,
  created_at timestamp with time zone,
  accepted_answer_id integer,
  score integer not null,
  last_active_at timestamp with time zone,
  views integer not null,
  link text not null,
  title text not null,
  account_id integer,
  foreign key (account_id) references account (id)
);


create table answer (
  id integer primary key,
  question_id integer not null,
  is_accepted boolean not null,
  score integer not null,
  last_active_at timestamp with time zone not null,
  created_at timestamp with time zone not null,
  account_id integer,
  foreign key (question_id) references question (id),
  foreign key (account_id) references account (id)
);


alter table question
  add constraint foreign_key_accepted_answer_id
  foreign key (accepted_answer_id) references answer (id)
;


create table tag (
  id text primary key
);


create table question_tag (
  question_id int not null,
  tag_id text not null,
  foreign key (question_id) references question (id),
  foreign key (tag_id) references tag (id)
);


create index on question_tag (question_id);
create index on question_tag (tag_id);

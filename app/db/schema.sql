Create Table if not exists expenses (

    id Integer Primary KEy Autoincrement,
    user_id text not null,
    ts text not null,
    amount real not null,
    currency text not null,
    category text not null,
    description text,
    merchant text,
    raw_text text,
    created_at text not null
);

create index if not exists idx_expenses_user_ts on expenses(user_id, ts);
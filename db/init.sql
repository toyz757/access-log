-- ログ情報
CREATE TABLE access_logs(
    log_id serial not null,
    remote_addr VARCHAR(40) not null,
    remote_user VARCHAR(20),
    time_iso8601 TIMESTAMP with time zone not null,
    request VARCHAR(40) not null,
    status INT not null,
    body_bytes_send INT not null,
    http_referer VARCHAR(40),
    http_user_agent VARCHAR(200),
    http_x_forwarded_for VARCHAR(40),
    primary key(log_id)
);

-- クエリパラメータ情報
CREATE TABLE query_param(
    log_id serial not null,
    query_name VARCHAR(40) not null,
    query_value VARCHAR(100) not null,
    primary key(log_id, query_name)
);
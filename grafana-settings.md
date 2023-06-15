# Grafanaの設定について

Grafanaのグラフ作成のためのSQLなどを保存しておくためのドキュメント

## SQL一覧

- 月毎のアクセス回数  

```sql
SELECT to_char(time_iso8601, 'YYYY/MM/dd') as date,
       count(*)
FROM access_logs 
GROUP BY date
ORDER BY date
```

- キーワードの検索回数

```sql
SELECT query_param.query_value as keyword, count(*) 
FROM access_logs INNER JOIN query_param 
ON access_logs.log_id = query_param.log_id
GROUP BY keyword;
```

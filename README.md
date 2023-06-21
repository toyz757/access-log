# README

## 概要

プロキシサーバのアクセスログを用いてアクセス状況の可視化を行う。

プロキシ経由でWebサーバにアクセスした際に、アクセスログを取得する。  
pythonをcronで実行することでPostgreSQLにアクセスログを保存する。  
GrafanaではPostgreSQLの値を用いてアクセス状況の可視化を行う。

![composite](resources/composite.drawio.svg)

## 利用方法

`docker-compose up -d`で起動することで各コンテナが起動し、以下のURLにアクセス可能になる。

- [apache httpd](localhost:8080)：Webサーバ
- [pgweb](localhost:8081)：PostgreSQLの可視化
- [Grafana](localhost:3000)：アクセスログの可視化

## ログについて

cronを利用して日単位でDBへのデータ挿入を行っている。  
そのため、直ちにサンプルデータが欲しい場合には、以下の手順が必要になる。

1. リバプロのコンテナ(rp)に入って、`logrotate -f /etc/logrotate.d/nginx`を実行。ログが作成される。
1. cronコンテナ(cron-server)に入って、nginx_log_pathの変数代入で`.`以降をコメントアウトする
1. cronコンテナ(cron-server)に入って、`python register.py`を実行。ログデータがPostgreSQLに保存される。
1. grafanaコンテナ(grafana)にアクセスして、データソース設定やグラフ設定を行う。

## Grafanaについて

[こちら](grafana-settings.md)を参照してください

## 注意点

- portの指定
  - リバプロに特定のポートを利用する場合は、単純なブラウザ起動ではブラウザからのアクセスができないため注意。
  - [参考リンク](https://www.ipentec.com/document/software-google-chrome-microsoft-edge-error-err-unsafe-port-accessing-on-port-10080)
- volumeの権限
  - volume先の権限によってログ出力がされないことがある。エラーも出ないため注意。

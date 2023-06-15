FROM postgres:15

# ロケールを設定する
ENV LANG ja_JP.UTF-8
ENV LC_COLLATE ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8

# 必要なパッケージをインストールする
RUN apt-get update && apt-get install -y locales locales-all

# ロケールを有効化する
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8

# DDLファイルの配置
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

# PostgreSQLを再起動する
RUN service postgresql restart

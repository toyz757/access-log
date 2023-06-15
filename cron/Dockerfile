FROM python:3.12.0a7-slim

ARG WORKDIR="/usr/src"
WORKDIR ${WORKDIR}

# 必要なパッケージのインストール
RUN apt-get update
RUN apt-get install -y cron

# cron設定ファイルのコピー
COPY cronjob /etc/cron.d/cronjob

# psycopg2-binaryインストールのために取得
RUN apt-get -y install libpq-dev build-essential

# 資材のコピー
COPY requirements.txt ${WORKDIR}/requirements.txt
COPY register.py ${WORKDIR}/register.py

# 必要なパッケージのインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# cronジョブを有効化
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

# cronのログ出力先を作成
RUN touch /var/log/cron.log

# コンテナ起動時にcronを実行するためのスクリプトを作成
RUN echo "cron && tail -f /var/log/cron.log" > /start.sh
RUN chmod +x /start.sh

# コンテナ起動時に/start.shを実行
CMD ["/bin/sh", "/start.sh"]

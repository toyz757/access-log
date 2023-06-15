FROM nginx:1.23.4

# ログローテーションコマンドの追加
RUN apt-get update
RUN apt -y install logrotate

# デフォルト設定を読ませないために削除
RUN rm -rf /etc/nginx/nginx.conf
# 設定ファイルのセット
COPY config/nginx.conf /etc/nginx/

# デフォルト設定を読ませないために削除
RUN rm -rf /etc/nginx/conf.d/default.conf
# 設定ファイルのセット
COPY config/proxy.conf.template /etc/nginx/templates/
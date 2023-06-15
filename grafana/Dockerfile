FROM grafana/grafana:9.5.2

USER root
RUN grafana-cli plugins install marcusolsson-csv-datasource

# ローカルのcsvファイルを読み込むための設定
RUN echo "[plugin.marcusolsson-csv-datasource]" >> /usr/share/grafana/conf/defaults.ini
RUN echo "allow_local_mode = true" >> /usr/share/grafana/conf/defaults.ini
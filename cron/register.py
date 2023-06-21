import os
import subprocess
import re
import psycopg2
from datetime import datetime
import urllib.parse
from user_agents import parse

# Nginxログファイルのディレクトリとファイル名のベース
nginx_log_dir = "/usr/src/log/"
nginx_log_base = "access.log"

# 日付の取得
today = datetime.now()
date_str = today.strftime("%Y%m%d")

# 実際のNginxログファイルパスを構築
nginx_log_path = nginx_log_dir + nginx_log_base #+ "." + date_str

# PostgreSQL接続情報
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

# ログファイルを開く
with open(nginx_log_path, "r") as file:
    cursor = conn.cursor()
    
    # ログファイルを1行ずつ処理する
    for line in file:
        # 正規表現を使ってログ行から必要な情報を抽出する
        regex_pattern = r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) "(.*?)" "(.*?)" "(.*?)"$'
        match = re.match(regex_pattern, line)
        
        if match:
            remote_addr = match.group(1)
            remote_user = match.group(2)
            time_iso8601 = datetime.strptime(match.group(4), "%d/%b/%Y:%H:%M:%S %z")
            request = match.group(6)
            parseRequest = urllib.parse.urlparse(request)
            url = parseRequest.netloc + parseRequest.path
            status = int(match.group(8))
            body_bytes_send = int(match.group(9))
            http_referer = match.group(10)
            http_user_agent = match.group(11)
            user_agent = parse(http_user_agent)
            browser_family = user_agent.browser.family
            browser_version = user_agent.browser.version_string
            user_os_family = user_agent.os.family
            user_os_version = user_agent.os.version_string
            user_device_family = user_agent.device.family
            http_x_forwarded_for = match.group(12)
            
            # アクセスログをaccess_logsテーブルに挿入する
            cursor.execute("""
                INSERT INTO access_logs (remote_addr, remote_user, time_iso8601, url, status, body_bytes_send, http_referer, browser_family, browser_version, user_os_family, user_os_version, user_device_family, http_x_forwarded_for)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (remote_addr, remote_user, time_iso8601, url, status, body_bytes_send, http_referer, browser_family, browser_version, user_os_family, user_os_version, user_device_family, http_x_forwarded_for))
            
            # クエリパラメータを解析して辞書に格納する
            query_params = urllib.parse.parse_qs(parseRequest.query)

            # クエリパラメータを表示する
            for key, values in query_params.items():
                for value in values:
                    cursor.execute("""
                        INSERT INTO query_param (log_id, query_name, query_value)
                        VALUES (currval('access_logs_log_id_seq'), %s, %s)
                    """, (key, value))
    
    # 変更をコミットして接続を閉じる
    conn.commit()
    conn.close()

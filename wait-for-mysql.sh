#!/bin/bash
# 等待MySQL服务就绪的脚本

set -e

host="${MYSQL_HOST:-mysql}"
port="${MYSQL_PORT:-3306}"
user="${MYSQL_USER:-onepiece_user}"
password="${MYSQL_PASSWORD:-onepiece_pass_2024}"

echo "⏳ 等待MySQL服务启动..."
echo "   主机: $host:$port"
echo "   用户: $user"

# 最多等待60次，每次2秒，共120秒
max_tries=60
count=0

until mysqladmin ping -h"$host" -P"$port" -u"$user" -p"$password" --silent > /dev/null 2>&1; do
  count=$((count + 1))
  if [ $count -ge $max_tries ]; then
    echo "❌ MySQL启动超时！"
    exit 1
  fi
  echo "   MySQL未就绪 - 等待中... ($count/$max_tries)"
  sleep 2
done

echo "✅ MySQL已就绪！正在启动Flask应用..."
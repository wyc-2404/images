#!/bin/bash
# deploy.sh - 短链接服务一键部署脚本

set -e

echo "=== 短链接服务部署脚本 ==="

# 变量配置
APP_DIR="/var/www/shorturl"
APP_USER="www-data"
DOMAIN=""

# 读取域名
read -p "请输入你的域名或IP: " DOMAIN

# 创建目录
echo "1. 创建应用目录..."
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

# 复制应用
echo "2. 复制应用文件..."
sudo cp -r /workspace/short_url_service/* $APP_DIR/
sudo chown -R $APP_USER:$APP_USER $APP_DIR

# 安装依赖
echo "3. 安装 Python 依赖..."
cd $APP_DIR
pip3 install -r requirements.txt gunicorn

# 配置 Gunicorn systemd 服务
echo "4. 配置 Gunicorn 服务..."
sudo tee /etc/systemd/system/shorturl.service > /dev/null <<EOF
[Unit]
Description=Short URL Service
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/gunicorn \
    --workers 3 \
    --bind unix:$APP_DIR/shorturl.sock \
    --access-logfile $APP_DIR/access.log \
    --error-logfile $APP_DIR/error.log \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 配置 Nginx
echo "5. 配置 Nginx..."
sudo tee /etc/nginx/sites-available/shorturl > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://unix:$APP_DIR/shorturl.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/shorturl /etc/nginx/sites-enabled/
sudo nginx -t

# 启动服务
echo "6. 启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable shorturl
sudo systemctl restart shorturl
sudo systemctl restart nginx

# 检查状态
echo "7. 检查服务状态..."
sudo systemctl status shorturl --no-pager

echo ""
echo "=== 部署完成！ ==="
echo "访问地址: http://$DOMAIN"
echo ""
echo "常用命令:"
echo "  查看状态: sudo systemctl status shorturl"
echo "  查看日志: sudo journalctl -u shorturl -f"
echo "  重启服务: sudo systemctl restart shorturl"

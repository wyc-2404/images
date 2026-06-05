#!/usr/bin/expect -f

set timeout 30
set host "39.106.212.63"
set port "22"
set user "root"
set password "Wei998598@"
set app_dir "/var/www/shorturl"

# 创建部署脚本
set deploy_script {
    set -e
    
    echo "=== 开始部署短链接服务 ==="
    
    # 创建目录
    mkdir -p /var/www/shorturl
    
    # 复制文件
    cp -r /tmp/shorturl/* /var/www/shorturl/
    
    # 安装依赖
    pip install flask flask-sqlalchemy hashids gunicorn
    
    # 配置Gunicorn服务
    cat > /etc/systemd/system/shorturl.service << 'EOF'
[Unit]
Description=Short URL Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/shorturl
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # 启动服务
    systemctl daemon-reload
    systemctl enable shorturl
    systemctl start shorturl
    
    # 配置防火墙
    firewall-cmd --zone=public --add-port=5000/tcp --permanent || true
    firewall-cmd --reload || true
    
    echo "=== 部署完成 ==="
    echo "服务地址: http://39.106.212.63:5000"
}

# 上传文件
spawn scp -P $port -r /workspace/short_url_service/* $user@$host:/tmp/shorturl/

expect {
    "password:" {
        send "$password\r"
        exp_continue
    }
    eof
}

# 执行部署命令
spawn ssh -p $port $user@$host "$deploy_script"

expect {
    "password:" {
        send "$password\r"
        exp_continue
    }
    eof
}

puts "部署完成!"

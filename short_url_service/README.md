# 短链接服务

一个基于 Python Flask + SQLite 的短链接生成服务。

## 功能特性

- ✅ 生成短链接
- ✅ 重定向到原始URL
- ✅ 访问统计
- ✅ 查看所有短链接
- ✅ 自动去重（相同URL返回相同短链）

## 安装

```bash
cd short_url_service
pip install -r requirements.txt
```

## 运行

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API 使用说明

### 1. 创建短链接

**请求:**
```bash
POST http://localhost:5000/api/shorten
Content-Type: application/json

{
  "url": "https://www.example.com/very/long/url/that/needs/to/be/shortened"
}
```

**响应:**
```json
{
  "short_url": "http://localhost:5000/jRk9xZ",
  "short_code": "jRk9xZ",
  "long_url": "https://www.example.com/very/long/url/that/needs/to/be/shortened"
}
```

### 2. 访问短链接（重定向）

**请求:**
```bash
GET http://localhost:5000/jRk9xZ
```

**响应:**
- 301 重定向到原始长链接

### 3. 查看统计信息

**请求:**
```bash
GET http://localhost:5000/api/stats/jRk9xZ
```

**响应:**
```json
{
  "short_code": "jRk9xZ",
  "short_url": "http://localhost:5000/jRk9xZ",
  "long_url": "https://www.example.com/...",
  "visits": 10,
  "created_at": "2024-01-15T10:30:00"
}
```

### 4. 列出所有短链接

**请求:**
```bash
GET http://localhost:5000/api/urls
```

**响应:**
```json
{
  "urls": [
    {
      "short_code": "jRk9xZ",
      "short_url": "http://localhost:5000/jRk9xZ",
      "long_url": "https://www.example.com/...",
      "visits": 10,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

## 测试示例

使用 curl 测试：

```bash
# 创建短链接
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# 访问短链接（会重定向）
curl -L http://localhost:5000/<short_code>

# 查看统计
curl http://localhost:5000/api/stats/<short_code>

# 列出所有
curl http://localhost:5000/api/urls
```

## 技术架构

- **Web框架**: Flask 3.0
- **ORM**: Flask-SQLAlchemy
- **数据库**: SQLite
- **短码生成**: Hashids（基于ID的62进制编码）

## 短码生成原理

1. 用户提交长URL
2. 数据库插入记录，获取自增ID
3. 使用 Hashids 将ID编码为6位短码（0-9, a-z, A-Z）
4. 返回短链接

优点：
- 短码长度固定且唯一
- 无法反向推导（安全性）
- 支持海量URL（62^6 ≈ 568亿）

## 生产环境建议

- 使用 Redis 缓存热门短链
- 使用 PostgreSQL/MySQL 替代 SQLite
- 添加 API 限流
- 添加用户认证
- 使用 Nginx 反向代理
- 配置 HTTPS

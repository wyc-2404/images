from flask import Flask, request, jsonify, redirect
from models import db, URLMapping
from utils import encode_id_to_short_code
import os

app = Flask(__name__)

# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'short_url.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 基础URL（可以根据需要修改）
BASE_URL = 'http://localhost:5000/'


@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        'message': '短链接服务已启动',
        'usage': {
            'create': 'POST /api/shorten with JSON body: {"url": "your_long_url"}',
            'redirect': 'GET /<short_code>',
            'stats': 'GET /api/stats/<short_code>'
        }
    })


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    创建短链接
    请求体: {"url": "长链接"}
    返回: {"short_url": "短链接", "short_code": "短码"}
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': '请提供url参数'}), 400
    
    long_url = data['url']
    
    # 检查URL是否已存在
    existing = URLMapping.query.filter_by(long_url=long_url).first()
    if existing:
        return jsonify({
            'short_url': BASE_URL + existing.short_code,
            'short_code': existing.short_code,
            'message': '该URL已存在'
        })
    
    # 创建新记录（先创建获取ID）
    new_mapping = URLMapping(long_url=long_url, short_code='temp')
    db.session.add(new_mapping)
    db.session.flush()  # 获取ID但不提交
    
    # 使用ID生成短码
    short_code = encode_id_to_short_code(new_mapping.id)
    new_mapping.short_code = short_code
    
    db.session.commit()
    
    return jsonify({
        'short_url': BASE_URL + short_code,
        'short_code': short_code,
        'long_url': long_url
    }), 201


@app.route('/<short_code>', methods=['GET'])
def redirect_to_long_url(short_code):
    """
    重定向到长链接
    """
    mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not mapping:
        return jsonify({'error': '短链接不存在'}), 404
    
    # 增加访问次数
    mapping.visits += 1
    db.session.commit()
    
    return redirect(mapping.long_url, code=301)


@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    """
    获取短链接统计信息
    """
    mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not mapping:
        return jsonify({'error': '短链接不存在'}), 404
    
    return jsonify({
        'short_code': mapping.short_code,
        'short_url': BASE_URL + mapping.short_code,
        'long_url': mapping.long_url,
        'visits': mapping.visits,
        'created_at': mapping.created_at.isoformat()
    })


@app.route('/api/urls', methods=['GET'])
def list_urls():
    """
    列出所有短链接
    """
    mappings = URLMapping.query.order_by(URLMapping.created_at.desc()).all()
    
    result = []
    for mapping in mappings:
        result.append({
            'short_code': mapping.short_code,
            'short_url': BASE_URL + mapping.short_code,
            'long_url': mapping.long_url,
            'visits': mapping.visits,
            'created_at': mapping.created_at.isoformat()
        })
    
    return jsonify({'urls': result, 'total': len(result)})


def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        print("数据库初始化完成")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

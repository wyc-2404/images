from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class URLMapping(db.Model):
    """短链接映射模型"""
    __tablename__ = 'url_mappings'
    
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)  # 原始长链接
    short_code = db.Column(db.String(10), unique=True, nullable=False)  # 短码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    visits = db.Column(db.Integer, default=0)  # 访问次数
    
    def __repr__(self):
        return f'<URLMapping {self.short_code} -> {self.long_url}>'

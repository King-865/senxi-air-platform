"""
数据库模型定义
使用 Flask-SQLAlchemy 管理数据库
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    username = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    
    # 用户等级和积分
    level = db.Column(db.String(10), default='L1')
    points = db.Column(db.Integer, default=0)
    
    # OAuth 登录信息
    wechat_openid = db.Column(db.String(100), unique=True, nullable=True)
    qq_openid = db.Column(db.String(100), unique=True, nullable=True)
    github_id = db.Column(db.String(100), unique=True, nullable=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    liked_posts = db.relationship('PostLike', backref='user', lazy='dynamic')
    favorited_posts = db.relationship('PostFavorite', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'phone': self.phone,
            'email': self.email,
            'username': self.username,
            'avatar': self.avatar,
            'level': self.level,
            'points': self.points,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Product(db.Model):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # home, office, car, accessory
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    
    # 库存管理
    stock = db.Column(db.Integer, default=0, nullable=False)
    sales = db.Column(db.Integer, default=0)
    
    # 产品信息
    description = db.Column(db.Text, nullable=True)
    main_image = db.Column(db.String(500), nullable=True)
    images = db.Column(db.Text, nullable=True)  # JSON 格式存储多张图片
    specs = db.Column(db.Text, nullable=True)  # JSON 格式存储规格参数
    features = db.Column(db.Text, nullable=True)  # JSON 格式存储特性列表
    tags = db.Column(db.Text, nullable=True)  # JSON 格式存储标签
    
    # 展示信息
    badge = db.Column(db.String(20), nullable=True)  # 角标文字
    badge_color = db.Column(db.String(20), nullable=True)  # 角标颜色
    rating = db.Column(db.Float, default=5.0)
    review_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def decrease_stock(self, quantity):
        """减少库存（销售）"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.sales += quantity
            return True
        return False
    
    def increase_stock(self, quantity):
        """增加库存（退货或补货）"""
        self.stock += quantity
        return True
    
    def to_dict(self):
        """转换为字典"""
        import json
        return {
            'id': self.id,
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'original_price': self.original_price,
            'stock': self.stock,
            'sales': self.sales,
            'description': self.description,
            'main_image': self.main_image,
            'images': json.loads(self.images) if self.images else [],
            'specs': json.loads(self.specs) if self.specs else {},
            'features': json.loads(self.features) if self.features else [],
            'tags': json.loads(self.tags) if self.tags else [],
            'badge': self.badge,
            'badge_color': self.badge_color,
            'rating': self.rating,
            'review_count': self.review_count,
        }


class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 订单信息
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, completed, cancelled
    
    # 收货信息
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(11), nullable=False)
    receiver_address = db.Column(db.String(500), nullable=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'receiver_address': self.receiver_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    """订单项模型"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 购买时的价格
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }


class Post(db.Model):
    """帖子模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # experience, formaldehyde, allergy, general
    images = db.Column(db.Text, nullable=True)  # JSON 格式存储图片列表
    
    # 统计数据
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    post_likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    post_favorites = db.relationship('PostFavorite', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        import json
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': self.author.to_dict() if self.author else None,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'images': json.loads(self.images) if self.images else [],
            'likes': self.likes,
            'views': self.views,
            'comment_count': self.comment_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    
    # 回复功能（可选）
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': self.author.to_dict() if self.author else None,
            'content': self.content,
            'likes': self.likes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PostLike(db.Model):
    """帖子点赞记录"""
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 确保同一用户对同一帖子只能点赞一次
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)


class PostFavorite(db.Model):
    """帖子收藏记录"""
    __tablename__ = 'post_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 确保同一用户对同一帖子只能收藏一次
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_favorite'),)

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
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Product(db.Model):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
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
    features = db.Column(db.Text, nullable=True)  # JSON 格式存储产品特点
    
    # 标签和徽章
    tags = db.Column(db.Text, nullable=True)  # JSON 格式存储标签
    badge = db.Column(db.String(50), nullable=True)
    badge_color = db.Column(db.String(20), nullable=True)
    
    # 评分
    rating = db.Column(db.Float, default=5.0)
    review_count = db.Column(db.Integer, default=0)
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        import json
        return {
            'id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'originalPrice': self.original_price,
            'stock': self.stock,
            'sales': self.sales,
            'description': self.description,
            'mainImage': self.main_image,
            'images': json.loads(self.images) if self.images else [],
            'specs': json.loads(self.specs) if self.specs else {},
            'features': json.loads(self.features) if self.features else [],
            'tags': json.loads(self.tags) if self.tags else [],
            'badge': self.badge,
            'badgeColor': self.badge_color,
            'rating': self.rating,
            'reviewCount': self.review_count,
        }
    
    def update_stock(self, quantity):
        """更新库存"""
        self.stock += quantity
        if self.stock < 0:
            self.stock = 0
    
    def decrease_stock(self, quantity):
        """减少库存（销售）"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.sales += quantity
            return True
        return False


class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 订单状态
    status = db.Column(db.String(20), default='pending', nullable=False)
    # pending: 待付款, paid: 已付款/待发货, shipped: 已发货/待收货, completed: 已完成, cancelled: 已取消
    
    # 金额
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    final_amount = db.Column(db.Float, nullable=False)
    
    # 收货信息
    receiver_name = db.Column(db.String(100), nullable=True)
    receiver_phone = db.Column(db.String(20), nullable=True)
    receiver_address = db.Column(db.String(500), nullable=True)
    
    # 备注
    remark = db.Column(db.Text, nullable=True)
    
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
            'id': self.order_id,
            'userId': self.user_id,
            'status': self.status,
            'totalAmount': self.total_amount,
            'discountAmount': self.discount_amount,
            'finalAmount': self.final_amount,
            'receiverName': self.receiver_name,
            'receiverPhone': self.receiver_phone,
            'receiverAddress': self.receiver_address,
            'remark': self.remark,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'paidAt': self.paid_at.isoformat() if self.paid_at else None,
            'shippedAt': self.shipped_at.isoformat() if self.shipped_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'items': [item.to_dict() for item in self.items],
        }


class OrderItem(db.Model):
    """订单项模型"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # 商品信息快照
    product_name = db.Column(db.String(200), nullable=False)
    product_image = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'productId': self.product_id,
            'productName': self.product_name,
            'productImage': self.product_image,
            'price': self.price,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
        }


class Post(db.Model):
    """社区帖子模型"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 帖子内容
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    # experience: 使用心得, formaldehyde: 除甲醛, allergy: 过敏防护, general: 综合讨论
    
    # 图片
    images = db.Column(db.Text, nullable=True)  # JSON 格式存储图片列表
    
    # 统计数据
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    
    # 状态
    is_published = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes_relation = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, current_user_id=None):
        """转换为字典"""
        import json
        is_liked = False
        if current_user_id:
            is_liked = PostLike.query.filter_by(
                post_id=self.id, 
                user_id=current_user_id
            ).first() is not None
        
        return {
            'id': self.post_id,
            'userId': self.user_id,
            'authorName': self.author.username or self.author.phone,
            'authorAvatar': self.author.avatar or 'https://i.pravatar.cc/100',
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'images': json.loads(self.images) if self.images else [],
            'likes': self.likes,
            'views': self.views,
            'commentsCount': self.comment_count,
            'isLiked': is_liked,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }


class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 评论内容
    content = db.Column(db.Text, nullable=False)
    
    # 回复
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    
    # 统计
    likes = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'postId': self.post_id,
            'userId': self.user_id,
            'authorName': self.author.username or self.author.phone,
            'authorAvatar': self.author.avatar or 'https://i.pravatar.cc/100',
            'content': self.content,
            'likes': self.likes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }


class PostLike(db.Model):
    """帖子点赞记录"""
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 唯一约束：一个用户只能给一个帖子点赞一次
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)

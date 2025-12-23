"""
数据库模型和管理
使用SQLite作为本地数据库
"""
import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'senxi.db')


def ensure_db_dir():
    """确保数据库目录存在"""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


@contextmanager
def get_db():
    """获取数据库连接"""
    ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """初始化数据库表"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                avatar TEXT,
                phone TEXT UNIQUE,
                auth_type TEXT DEFAULT 'phone',
                level INTEGER DEFAULT 1,
                points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 商品表（含库存）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                original_price REAL,
                category TEXT,
                main_image TEXT,
                images TEXT,
                tags TEXT,
                specs TEXT,
                features TEXT,
                stock INTEGER DEFAULT 0,
                sales INTEGER DEFAULT 0,
                rating REAL DEFAULT 5.0,
                reviews_count INTEGER DEFAULT 0,
                badge TEXT,
                badge_color TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 订单表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                shipping_address TEXT,
                shipping_name TEXT,
                shipping_phone TEXT,
                payment_method TEXT,
                paid_at TIMESTAMP,
                shipped_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # 订单项表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                product_image TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # 购物车表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE(user_id, product_id)
            )
        ''')
        
        # 社区帖子表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                images TEXT,
                category TEXT DEFAULT 'general',
                likes INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # 帖子评论表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                parent_id INTEGER,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (parent_id) REFERENCES comments(id)
            )
        ''')
        
        # 点赞记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, target_type, target_id)
            )
        ''')
        
        # 收藏表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE(user_id, product_id)
            )
        ''')
        
        # 收货地址表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                province TEXT NOT NULL,
                city TEXT NOT NULL,
                district TEXT NOT NULL,
                detail TEXT NOT NULL,
                is_default INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        
        # 初始化示例商品数据
        _init_sample_products(cursor, conn)


def _init_sample_products(cursor, conn):
    """初始化示例商品数据"""
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] > 0:
        return  # 已有数据，跳过
    
    products = [
        {
            'id': 'prod_001',
            'name': '净界者·森林呼吸Pro',
            'description': '采用H13级HEPA滤网，配合光触媒分解技术，高效去除PM2.5、甲醛、细菌病毒。适合40-60㎡空间使用。',
            'price': 2999,
            'original_price': 3599,
            'category': 'home',
            'main_image': 'https://via.placeholder.com/400x400?text=Forest+Pro',
            'images': json.dumps(['https://via.placeholder.com/400x400?text=Image1', 'https://via.placeholder.com/400x400?text=Image2']),
            'tags': json.dumps(['除甲醛', '除PM2.5', '智能控制', '静音']),
            'specs': json.dumps({
                'area': '40-60㎡',
                'cadr': '500m³/h',
                'formaldehyde_cadr': '300m³/h',
                'noise': '22-58dB',
                'filter_level': 'HEPA H13',
                'power': '55W',
                'dimensions': '350×350×680mm',
                'weight': '9.5kg',
                'smart_features': 'APP控制、语音控制、空气质量监测'
            }),
            'features': json.dumps([
                {'icon': 'shield', 'title': 'H13级HEPA滤网', 'description': '过滤99.97%的0.3微米颗粒物'},
                {'icon': 'zap', 'title': '光触媒分解', 'description': '主动分解甲醛、TVOC等有害气体'},
                {'icon': 'wifi', 'title': '智能互联', 'description': 'APP远程控制，支持小爱同学/天猫精灵'},
                {'icon': 'moon', 'title': '超静音设计', 'description': '睡眠模式仅22分贝，安心入眠'}
            ]),
            'stock': 500,
            'sales': 1256,
            'rating': 4.9,
            'reviews_count': 328,
            'badge': '热销',
            'badge_color': 'red'
        },
        {
            'id': 'prod_002',
            'name': '净界者·清新之风Max',
            'description': '旗舰级空气净化器，双风道设计，CADR值高达800m³/h，适合60-100㎡大空间使用。',
            'price': 4999,
            'original_price': 5999,
            'category': 'home',
            'main_image': 'https://via.placeholder.com/400x400?text=Fresh+Max',
            'images': json.dumps(['https://via.placeholder.com/400x400?text=Image1']),
            'tags': json.dumps(['大户型', '双风道', '高CADR', '智能']),
            'specs': json.dumps({
                'area': '60-100㎡',
                'cadr': '800m³/h',
                'formaldehyde_cadr': '500m³/h',
                'noise': '25-65dB',
                'filter_level': 'HEPA H13',
                'power': '75W',
                'dimensions': '400×400×780mm',
                'weight': '12kg',
                'smart_features': 'APP控制、语音控制、空气质量监测、滤芯寿命提醒'
            }),
            'features': json.dumps([
                {'icon': 'wind', 'title': '双风道设计', 'description': '360°进风，快速净化全屋空气'},
                {'icon': 'activity', 'title': '高效净化', 'description': 'CADR值800m³/h，10分钟净化60㎡'},
                {'icon': 'smartphone', 'title': '智能APP', 'description': '实时监测，远程控制，滤芯提醒'},
                {'icon': 'award', 'title': '权威认证', 'description': '通过中国家电研究院检测认证'}
            ]),
            'stock': 200,
            'sales': 856,
            'rating': 4.8,
            'reviews_count': 215,
            'badge': '旗舰',
            'badge_color': 'purple'
        },
        {
            'id': 'prod_003',
            'name': '净界者·守护天使',
            'description': '专为母婴设计，采用医疗级净化标准，超静音运行，守护宝宝健康呼吸。',
            'price': 3499,
            'original_price': 3999,
            'category': 'home',
            'main_image': 'https://via.placeholder.com/400x400?text=Angel',
            'images': json.dumps(['https://via.placeholder.com/400x400?text=Image1']),
            'tags': json.dumps(['母婴', '医疗级', '超静音', '无臭氧']),
            'specs': json.dumps({
                'area': '30-50㎡',
                'cadr': '400m³/h',
                'formaldehyde_cadr': '200m³/h',
                'noise': '20-52dB',
                'filter_level': 'HEPA H13 + 活性炭',
                'power': '45W',
                'dimensions': '320×320×620mm',
                'weight': '8kg',
                'smart_features': 'APP控制、童锁、夜灯模式'
            }),
            'features': json.dumps([
                {'icon': 'baby', 'title': '母婴专属', 'description': '医疗级净化标准，无臭氧释放'},
                {'icon': 'volume-x', 'title': '超静音', 'description': '睡眠模式仅20分贝，不打扰宝宝'},
                {'icon': 'lock', 'title': '童锁保护', 'description': '防止宝宝误触，安全放心'},
                {'icon': 'sun', 'title': '柔和夜灯', 'description': '可调节亮度，陪伴宝宝入睡'}
            ]),
            'stock': 300,
            'sales': 623,
            'rating': 4.9,
            'reviews_count': 189,
            'badge': '母婴优选',
            'badge_color': 'pink'
        },
        {
            'id': 'prod_004',
            'name': '净界者·车载清风',
            'description': '车载空气净化器，小巧便携，USB供电，快速净化车内空气。',
            'price': 599,
            'original_price': 799,
            'category': 'car',
            'main_image': 'https://via.placeholder.com/400x400?text=Car+Air',
            'images': json.dumps(['https://via.placeholder.com/400x400?text=Image1']),
            'tags': json.dumps(['车载', '便携', 'USB供电', '除异味']),
            'specs': json.dumps({
                'area': '车内空间',
                'cadr': '30m³/h',
                'noise': '≤35dB',
                'filter_level': 'HEPA H11',
                'power': '5W',
                'dimensions': '80×80×180mm',
                'weight': '0.5kg',
                'smart_features': '一键开关、滤芯更换提醒'
            }),
            'features': json.dumps([
                {'icon': 'car', 'title': '车载专用', 'description': '专为车内空间设计，小巧不占位'},
                {'icon': 'usb', 'title': 'USB供电', 'description': '车载USB即可供电，方便使用'},
                {'icon': 'wind', 'title': '快速净化', 'description': '5分钟净化车内空气'},
                {'icon': 'droplet', 'title': '除异味', 'description': '有效去除烟味、异味'}
            ]),
            'stock': 1000,
            'sales': 2156,
            'rating': 4.7,
            'reviews_count': 523,
            'badge': '热销',
            'badge_color': 'orange'
        },
        {
            'id': 'prod_005',
            'name': 'H13级HEPA复合滤芯',
            'description': '适用于净界者·森林呼吸Pro，建议6-12个月更换一次。',
            'price': 299,
            'original_price': 399,
            'category': 'accessory',
            'main_image': 'https://via.placeholder.com/400x400?text=Filter',
            'images': json.dumps(['https://via.placeholder.com/400x400?text=Image1']),
            'tags': json.dumps(['滤芯', 'H13', '原装']),
            'specs': json.dumps({
                'compatible': '净界者·森林呼吸Pro',
                'filter_level': 'HEPA H13 + 活性炭',
                'lifespan': '6-12个月',
                'dimensions': '300×300×50mm'
            }),
            'features': json.dumps([
                {'icon': 'check', 'title': '原装品质', 'description': '官方原装滤芯，品质保证'},
                {'icon': 'shield', 'title': 'H13级别', 'description': '过滤99.97%的0.3微米颗粒物'}
            ]),
            'stock': 2000,
            'sales': 3256,
            'rating': 4.9,
            'reviews_count': 856,
            'badge': None,
            'badge_color': None
        }
    ]
    
    for p in products:
        cursor.execute('''
            INSERT INTO products (id, name, description, price, original_price, category, 
                main_image, images, tags, specs, features, stock, sales, rating, 
                reviews_count, badge, badge_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p['id'], p['name'], p['description'], p['price'], p['original_price'],
            p['category'], p['main_image'], p['images'], p['tags'], p['specs'],
            p['features'], p['stock'], p['sales'], p['rating'], p['reviews_count'],
            p['badge'], p['badge_color']
        ))
    
    conn.commit()


class UserDB:
    """用户数据库操作"""
    
    @staticmethod
    def create(user_id: str, nickname: str, phone: str = None, 
               avatar: str = None, auth_type: str = 'phone') -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (id, nickname, phone, avatar, auth_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, nickname, phone, avatar, auth_type))
            conn.commit()
            return UserDB.get_by_id(user_id)
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_by_phone(phone: str) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def update_points(user_id: str, points: int):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET points = points + ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (points, user_id))
            conn.commit()


class ProductDB:
    """商品数据库操作"""
    
    @staticmethod
    def get_all(category: str = None, status: str = 'active') -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute('''
                    SELECT * FROM products WHERE status = ? AND category = ?
                    ORDER BY sales DESC
                ''', (status, category))
            else:
                cursor.execute('''
                    SELECT * FROM products WHERE status = ?
                    ORDER BY sales DESC
                ''', (status,))
            rows = cursor.fetchall()
            return [ProductDB._parse_product(dict(row)) for row in rows]
    
    @staticmethod
    def get_by_id(product_id: str) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            return ProductDB._parse_product(dict(row)) if row else None
    
    @staticmethod
    def check_stock(product_id: str, quantity: int) -> bool:
        """检查库存是否充足"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT stock FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            return row and row['stock'] >= quantity
    
    @staticmethod
    def reduce_stock(product_id: str, quantity: int) -> bool:
        """减少库存"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products SET stock = stock - ?, sales = sales + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND stock >= ?
            ''', (quantity, quantity, product_id, quantity))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def _parse_product(product: Dict) -> Dict:
        """解析JSON字段"""
        for field in ['images', 'tags', 'specs', 'features']:
            if product.get(field):
                try:
                    product[field] = json.loads(product[field])
                except:
                    pass
        return product


class OrderDB:
    """订单数据库操作"""
    
    @staticmethod
    def create(user_id: str, items: List[Dict], shipping_info: Dict) -> Optional[str]:
        """创建订单"""
        import uuid
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # 计算总金额并检查库存
            total_amount = 0
            for item in items:
                product = ProductDB.get_by_id(item['product_id'])
                if not product:
                    return None
                if not ProductDB.check_stock(item['product_id'], item['quantity']):
                    return None
                total_amount += product['price'] * item['quantity']
            
            # 创建订单
            cursor.execute('''
                INSERT INTO orders (id, user_id, total_amount, shipping_address, 
                    shipping_name, shipping_phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                order_id, user_id, total_amount,
                shipping_info.get('address', ''),
                shipping_info.get('name', ''),
                shipping_info.get('phone', '')
            ))
            
            # 创建订单项并减少库存
            for item in items:
                product = ProductDB.get_by_id(item['product_id'])
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, product_name, 
                        product_image, price, quantity)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    order_id, item['product_id'], product['name'],
                    product['main_image'], product['price'], item['quantity']
                ))
                ProductDB.reduce_stock(item['product_id'], item['quantity'])
            
            conn.commit()
            return order_id
    
    @staticmethod
    def get_user_orders(user_id: str, status: str = None) -> List[Dict]:
        """获取用户订单列表"""
        with get_db() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('''
                    SELECT * FROM orders WHERE user_id = ? AND status = ?
                    ORDER BY created_at DESC
                ''', (user_id, status))
            else:
                cursor.execute('''
                    SELECT * FROM orders WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
            orders = [dict(row) for row in cursor.fetchall()]
            
            # 获取订单项
            for order in orders:
                cursor.execute('''
                    SELECT * FROM order_items WHERE order_id = ?
                ''', (order['id'],))
                order['items'] = [dict(row) for row in cursor.fetchall()]
            
            return orders
    
    @staticmethod
    def get_by_id(order_id: str) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            row = cursor.fetchone()
            if not row:
                return None
            order = dict(row)
            cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,))
            order['items'] = [dict(r) for r in cursor.fetchall()]
            return order
    
    @staticmethod
    def update_status(order_id: str, status: str):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, order_id))
            conn.commit()


class PostDB:
    """帖子数据库操作"""
    
    @staticmethod
    def create(user_id: str, title: str, content: str, 
               category: str = 'general', images: List[str] = None) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO posts (user_id, title, content, category, images)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, title, content, category, json.dumps(images or [])))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_all(category: str = None, limit: int = 20, offset: int = 0) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute('''
                    SELECT p.*, u.nickname as author_name, u.avatar as author_avatar
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.status = 'active' AND p.category = ?
                    ORDER BY p.created_at DESC
                    LIMIT ? OFFSET ?
                ''', (category, limit, offset))
            else:
                cursor.execute('''
                    SELECT p.*, u.nickname as author_name, u.avatar as author_avatar
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.status = 'active'
                    ORDER BY p.created_at DESC
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
            posts = [dict(row) for row in cursor.fetchall()]
            for post in posts:
                if post.get('images'):
                    try:
                        post['images'] = json.loads(post['images'])
                    except:
                        pass
            return posts
    
    @staticmethod
    def get_user_posts(user_id: str) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM posts WHERE user_id = ? AND status = 'active'
                ORDER BY created_at DESC
            ''', (user_id,))
            posts = [dict(row) for row in cursor.fetchall()]
            for post in posts:
                if post.get('images'):
                    try:
                        post['images'] = json.loads(post['images'])
                    except:
                        pass
            return posts
    
    @staticmethod
    def get_by_id(post_id: int) -> Optional[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.nickname as author_name, u.avatar as author_avatar
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            ''', (post_id,))
            row = cursor.fetchone()
            if not row:
                return None
            post = dict(row)
            if post.get('images'):
                try:
                    post['images'] = json.loads(post['images'])
                except:
                    pass
            return post
    
    @staticmethod
    def increment_views(post_id: int):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE posts SET views = views + 1 WHERE id = ?', (post_id,))
            conn.commit()
    
    @staticmethod
    def like(post_id: int, user_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO likes (user_id, target_type, target_id)
                    VALUES (?, 'post', ?)
                ''', (user_id, post_id))
                cursor.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False


class CommentDB:
    """评论数据库操作"""
    
    @staticmethod
    def create(post_id: int, user_id: str, content: str, parent_id: int = None) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comments (post_id, user_id, content, parent_id)
                VALUES (?, ?, ?, ?)
            ''', (post_id, user_id, content, parent_id))
            cursor.execute('UPDATE posts SET comments_count = comments_count + 1 WHERE id = ?', (post_id,))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_post_comments(post_id: int) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, u.nickname as author_name, u.avatar as author_avatar
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.created_at ASC
            ''', (post_id,))
            return [dict(row) for row in cursor.fetchall()]


# 初始化数据库
init_database()

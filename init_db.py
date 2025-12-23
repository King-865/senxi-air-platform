"""
数据库初始化脚本
用于创建数据库表并填充示例数据
"""

from app import app, db
from models import User, Product, Post, Comment
from datetime import datetime
import json


def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表（谨慎使用）
        print("正在删除现有数据库表...")
        db.drop_all()
        
        # 创建所有表
        print("正在创建数据库表...")
        db.create_all()
        
        # 添加示例用户
        print("正在添加示例用户...")
        users = [
            User(
                phone='13800138001',
                username='清新小屋',
                level='L2',
                points=1280,
                avatar='https://i.pravatar.cc/100?img=1'
            ),
            User(
                phone='13800138002',
                username='过敏星人',
                level='L1',
                points=560,
                avatar='https://i.pravatar.cc/100?img=2'
            ),
            User(
                phone='13800138003',
                username='科技宅',
                level='L3',
                points=2350,
                avatar='https://i.pravatar.cc/100?img=3'
            ),
            User(
                phone='13800138004',
                username='宝妈日记',
                level='L2',
                points=980,
                avatar='https://i.pravatar.cc/100?img=4'
            ),
        ]
        
        for user in users:
            user.set_password('123456')  # 设置默认密码
            db.session.add(user)
        
        db.session.commit()
        print(f"已添加 {len(users)} 个示例用户")
        
        # 添加示例产品
        print("正在添加示例产品...")
        products = [
            Product(
                product_id='prod_001',
                name='净界者·森林呼吸Pro',
                category='home',
                price=2999,
                original_price=3999,
                stock=50,
                sales=1256,
                description='旗舰级家用空气净化器，采用H13级HEPA滤网，CADR值高达800m³/h，适用于60-100㎡大空间。智能检测PM2.5、甲醛、VOC等多项指标，APP远程控制，静音运行。',
                main_image='https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800',
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
                ]),
                specs=json.dumps({
                    '适用面积': '60-100㎡',
                    'CADR值': '800m³/h',
                    '滤网等级': 'H13级HEPA',
                    '噪音': '20-65dB',
                    '功率': '60W',
                    '尺寸': '380×380×680mm',
                    '净重': '12kg'
                }),
                features=json.dumps([
                    {'title': 'H13级HEPA滤网', 'description': '过滤效率99.97%，有效去除PM2.5、花粉、细菌'},
                    {'title': '智能传感器', 'description': '实时监测空气质量，自动调节净化模式'},
                    {'title': '静音设计', 'description': '睡眠模式低至20分贝，不影响休息'},
                    {'title': 'APP远程控制', 'description': '随时随地掌控家中空气质量'}
                ]),
                tags=json.dumps(['旗舰款', '智能互联', '大空间', '除甲醛']),
                badge='热销',
                badge_color='#EF4444',
                rating=4.9,
                review_count=523
            ),
            Product(
                product_id='prod_002',
                name='净界者·清新之风Max',
                category='home',
                price=4999,
                stock=30,
                sales=856,
                description='专业级空气净化器，双重过滤系统，CADR值1000m³/h，适用于100㎡以上超大空间。配备紫外线杀菌、负离子发生器，全方位守护家人健康。',
                main_image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
                ]),
                specs=json.dumps({
                    '适用面积': '100-150㎡',
                    'CADR值': '1000m³/h',
                    '滤网等级': 'H13级HEPA+活性炭',
                    '噪音': '22-68dB',
                    '功率': '80W',
                    '尺寸': '420×420×750mm',
                    '净重': '15kg'
                }),
                features=json.dumps([
                    {'title': '双重过滤系统', 'description': 'HEPA+活性炭双层过滤，深度净化'},
                    {'title': '紫外线杀菌', 'description': 'UV-C紫外线杀菌，消灭细菌病毒'},
                    {'title': '负离子发生器', 'description': '释放负离子，清新空气'},
                    {'title': '超大CADR值', 'description': '1000m³/h大风量，快速净化'}
                ]),
                tags=json.dumps(['专业级', '超大空间', '杀菌', '负离子']),
                badge='新品',
                badge_color='#3B82F6',
                rating=4.8,
                review_count=342
            ),
            Product(
                product_id='prod_003',
                name='净界者·守护天使',
                category='baby',
                price=1899,
                stock=80,
                sales=2134,
                description='专为母婴设计的空气净化器，H13级医疗级滤网，超静音设计，睡眠模式仅18分贝。智能夜灯功能，守护宝宝每一个安心夜晚。',
                main_image='https://images.unsplash.com/photo-1527089969914-c5c5e0e8c7c1?w=800',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1527089969914-c5c5e0e8c7c1?w=800'
                ]),
                specs=json.dumps({
                    '适用面积': '20-40㎡',
                    'CADR值': '400m³/h',
                    '滤网等级': 'H13级医疗级HEPA',
                    '噪音': '18-55dB',
                    '功率': '35W',
                    '尺寸': '280×280×550mm',
                    '净重': '6kg'
                }),
                features=json.dumps([
                    {'title': '医疗级滤网', 'description': 'H13级医疗级HEPA，安全可靠'},
                    {'title': '超静音设计', 'description': '睡眠模式仅18分贝，不打扰宝宝'},
                    {'title': '智能夜灯', 'description': '柔和夜灯，方便夜间照顾宝宝'},
                    {'title': '童锁保护', 'description': '防止宝宝误操作，安全贴心'}
                ]),
                tags=json.dumps(['母婴专用', '超静音', '医疗级', '夜灯']),
                badge='推荐',
                badge_color='#10B981',
                rating=4.9,
                review_count=1245
            ),
            Product(
                product_id='prod_004',
                name='净界者·车载清风',
                category='car',
                price=599,
                stock=120,
                sales=3456,
                description='车载空气净化器，小巧便携，USB供电。H11级HEPA滤网，有效去除车内异味、甲醛、PM2.5。负离子功能，让车内空气更清新。',
                main_image='https://images.unsplash.com/photo-1464219789935-c2d9d9aba644?w=800',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1464219789935-c2d9d9aba644?w=800'
                ]),
                specs=json.dumps({
                    '适用空间': '车内',
                    'CADR值': '15m³/h',
                    '滤网等级': 'H11级HEPA',
                    '噪音': '25-45dB',
                    '功率': '5W',
                    '尺寸': '80×80×180mm',
                    '净重': '0.3kg'
                }),
                features=json.dumps([
                    {'title': 'USB供电', 'description': '车载USB接口供电，即插即用'},
                    {'title': '小巧便携', 'description': '体积小巧，不占空间'},
                    {'title': '负离子功能', 'description': '释放负离子，清新空气'},
                    {'title': '去除异味', 'description': '有效去除车内烟味、异味'}
                ]),
                tags=json.dumps(['车载', '便携', '负离子', 'USB供电']),
                rating=4.7,
                review_count=2156
            ),
            Product(
                product_id='prod_005',
                name='H13级HEPA复合滤芯',
                category='accessory',
                price=299,
                stock=200,
                sales=5678,
                description='原装H13级HEPA复合滤芯，适配森林呼吸Pro、清新之风Max等型号。建议每6-12个月更换一次，保持最佳净化效果。',
                main_image='https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400'
                ]),
                specs=json.dumps({
                    '滤网等级': 'H13级HEPA',
                    '适配型号': '森林呼吸Pro、清新之风Max',
                    '使用寿命': '6-12个月',
                    '过滤效率': '99.97%',
                    '材质': 'HEPA+活性炭'
                }),
                features=json.dumps([
                    {'title': '原装正品', 'description': '官方原装滤芯，品质保证'},
                    {'title': 'H13级HEPA', 'description': '过滤效率99.97%'},
                    {'title': '复合滤芯', 'description': 'HEPA+活性炭双重过滤'},
                    {'title': '易于更换', 'description': '简单操作，轻松更换'}
                ]),
                tags=json.dumps(['滤芯', '原装', 'H13级', '耗材']),
                rating=4.8,
                review_count=3421
            ),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print(f"已添加 {len(products)} 个示例产品")
        
        # 添加示例帖子
        print("正在添加示例帖子...")
        posts = [
            Post(
                post_id='post_001',
                user_id=1,
                title='新房除甲醛三个月心得分享',
                content='入住新房前买了森林呼吸Pro，连续开了三个月，甲醛从0.15降到了0.03，效果真的很明显！分享一下我的使用经验...',
                category='formaldehyde',
                images=json.dumps(['https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400']),
                likes=256,
                views=1520,
                comment_count=45,
                created_at=datetime(2024, 12, 15, 10, 30, 0)
            ),
            Post(
                post_id='post_002',
                user_id=2,
                title='过敏体质的救星！用了半年的真实感受',
                content='作为一个对花粉和灰尘严重过敏的人，自从用了净界者之后，在家基本不打喷嚏了。特别是春天花粉季节，简直是救命神器...',
                category='allergy',
                likes=189,
                views=980,
                comment_count=32,
                created_at=datetime(2024, 12, 14, 15, 20, 0)
            ),
            Post(
                post_id='post_003',
                user_id=3,
                title='清新之风Max开箱评测',
                content='刚收到旗舰款，做个开箱评测。包装很扎实，机器质感很好，白色外观很百搭。开机测试了一下，风量确实很大...',
                category='experience',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
                    'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400'
                ]),
                likes=342,
                views=2100,
                comment_count=67,
                created_at=datetime(2024, 12, 13, 9, 0, 0)
            ),
            Post(
                post_id='post_004',
                user_id=4,
                title='给宝宝房间选的守护天使，太安静了',
                content='宝宝房间一直想买个空气净化器，对比了很多款，最后选了守护天使。最大的感受就是真的很安静，宝宝睡觉完全不受影响...',
                category='experience',
                images=json.dumps(['https://images.unsplash.com/photo-1527089969914-c5c5e0e8c7c1?w=400']),
                likes=421,
                views=1850,
                comment_count=53,
                created_at=datetime(2024, 12, 12, 14, 45, 0)
            ),
        ]
        
        for post in posts:
            db.session.add(post)
        
        db.session.commit()
        print(f"已添加 {len(posts)} 个示例帖子")
        
        print("\n数据库初始化完成！")
        print(f"用户数: {User.query.count()}")
        print(f"产品数: {Product.query.count()}")
        print(f"帖子数: {Post.query.count()}")
        print("\n默认用户密码: 123456")


if __name__ == '__main__':
    init_database()

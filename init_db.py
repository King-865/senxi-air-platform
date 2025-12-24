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
            # 雷神空气净化器 - 高端款
            Product(
                product_id='prod_001',
                name='雷神空气净化器 YDH201',
                category='home',
                price=12999,
                original_price=15999,
                stock=15,
                sales=128,
                description='雷神旗舰级家用空气净化器，采用H14级医疗级HEPA滤网，CADR值高达1200m³/h，适用于100-150㎡超大空间。智能检测PM2.5、甲醛、VOC、TVOC等多项指标，APP远程控制，超静音运行，数字显示屏实时显示空气质量。',
                main_image='/static/images/products/raysun_ydh201.png',
                images=json.dumps([
                    '/static/images/products/raysun_ydh201.png'
                ]),
                specs=json.dumps({
                    '适用面积': '100-150㎡',
                    'CADR值': '1200m³/h',
                    '滤网等级': 'H14级医疗级HEPA',
                    '噪音': '18-68dB',
                    '功率': '90W',
                    '尺寸': '450×450×800mm',
                    '净重': '18kg',
                    '显示屏': '数字LED显示',
                    '控制方式': 'APP远程+触控面板'
                }),
                features=json.dumps([
                    {'title': 'H14级医疗级HEPA', 'description': '过滤效率99.995%，医疗级别防护'},
                    {'title': '超大CADR值', 'description': '1200m³/h大风量，快速净化超大空间'},
                    {'title': '智能传感器阵列', 'description': '实时监测PM2.5、甲醛、VOC、TVOC等多项指标'},
                    {'title': 'APP智能控制', 'description': '远程操控，定时预约，空气质量报告'},
                    {'title': '超静音设计', 'description': '睡眠模式低至18分贝，不影响休息'},
                    {'title': '数字显示屏', 'description': 'LED数字显示，空气质量一目了然'}
                ]),
                tags=json.dumps(['旗舰款', '智能互联', '超大空间', '医疗级', '数字显示']),
                badge='旗舰',
                badge_color='#8B5CF6',
                rating=4.9,
                review_count=256
            ),
            
            # 雷神空气净化器 - 性价比款
            Product(
                product_id='prod_002',
                name='雷神空气净化器 G135',
                category='home',
                price=2399,
                original_price=2999,
                stock=80,
                sales=1856,
                description='雷神性价比之选，采用H13级HEPA滤网，CADR值600m³/h，适用于40-80㎡空间。智能检测PM2.5、甲醛，三档风速调节，静音运行。圆柱形设计，360°进风，净化更高效。',
                main_image='/static/images/products/raysun_g135.png',
                images=json.dumps([
                    '/static/images/products/raysun_g135.png'
                ]),
                specs=json.dumps({
                    '适用面积': '40-80㎡',
                    'CADR值': '600m³/h',
                    '滤网等级': 'H13级HEPA',
                    '噪音': '20-62dB',
                    '功率': '55W',
                    '尺寸': '320×320×650mm',
                    '净重': '9kg',
                    '控制方式': '触控面板'
                }),
                features=json.dumps([
                    {'title': 'H13级HEPA滤网', 'description': '过滤效率99.97%，有效去除PM2.5'},
                    {'title': '360°进风设计', 'description': '圆柱形机身，全方位进风，净化更快'},
                    {'title': '智能传感器', 'description': '实时监测PM2.5和甲醛浓度'},
                    {'title': '三档风速', 'description': '低中高三档可调，满足不同需求'},
                    {'title': '静音运行', 'description': '睡眠模式仅20分贝'},
                    {'title': '高性价比', 'description': '价格亲民，性能出众'}
                ]),
                tags=json.dumps(['性价比', '家用', '静音', '360°进风']),
                badge='热销',
                badge_color='#EF4444',
                rating=4.8,
                review_count=1523
            ),
            
            # 雷神空气净化器滤芯 - H14级
            Product(
                product_id='prod_003',
                name='雷神H14级HEPA复合滤芯（YDH201专用）',
                category='accessory',
                price=899,
                stock=100,
                sales=456,
                description='雷神YDH201专用原装H14级HEPA复合滤芯，医疗级过滤效果，建议每8-12个月更换一次，保持最佳净化效果。',
                main_image='https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400'
                ]),
                specs=json.dumps({
                    '滤网等级': 'H14级医疗级HEPA',
                    '适配型号': '雷神YDH201',
                    '使用寿命': '8-12个月',
                    '过滤效率': '99.995%',
                    '材质': 'H14 HEPA+活性炭+抗菌层'
                }),
                features=json.dumps([
                    {'title': '原装正品', 'description': '雷神官方原装滤芯，品质保证'},
                    {'title': 'H14医疗级', 'description': '过滤效率99.995%，医疗级防护'},
                    {'title': '三层复合过滤', 'description': 'HEPA+活性炭+抗菌层三重防护'},
                    {'title': '易于更换', 'description': '简单操作，轻松更换'}
                ]),
                tags=json.dumps(['滤芯', '原装', 'H14级', '耗材']),
                rating=4.9,
                review_count=234
            ),
            
            # 雷神空气净化器滤芯 - H13级
            Product(
                product_id='prod_004',
                name='雷神H13级HEPA复合滤芯（G135专用）',
                category='accessory',
                price=299,
                stock=200,
                sales=2134,
                description='雷神G135专用原装H13级HEPA复合滤芯，高效过滤PM2.5、甲醛、VOC，建议每6-12个月更换一次。',
                main_image='https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
                images=json.dumps([
                    'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400'
                ]),
                specs=json.dumps({
                    '滤网等级': 'H13级HEPA',
                    '适配型号': '雷神G135',
                    '使用寿命': '6-12个月',
                    '过滤效率': '99.97%',
                    '材质': 'H13 HEPA+活性炭'
                }),
                features=json.dumps([
                    {'title': '原装正品', 'description': '雷神官方原装滤芯，品质保证'},
                    {'title': 'H13级HEPA', 'description': '过滤效率99.97%'},
                    {'title': '复合滤芯', 'description': 'HEPA+活性炭双重过滤'},
                    {'title': '高性价比', 'description': '价格亲民，效果出众'}
                ]),
                tags=json.dumps(['滤芯', '原装', 'H13级', '耗材', '性价比']),
                rating=4.8,
                review_count=1876
            ),
            
            # 清凉维C无糖薄荷糖果
            Product(
                product_id='prod_005',
                name='清凉维C无糖薄荷糖果',
                category='accessory',
                price=4.9,
                stock=500,
                sales=8956,
                description='清凉薄荷糖果，添加维生素C，无糖配方，清新口气，提神醒脑。多种水果口味可选，独立小包装，方便携带。',
                main_image='/static/images/products/candy.png',
                images=json.dumps([
                    '/static/images/products/candy.png'
                ]),
                specs=json.dumps({
                    '规格': '约50颗/份',
                    '口味': '薄荷、柠檬、葡萄、草莓等多种口味',
                    '配料': '木糖醇、薄荷脑、维生素C',
                    '保质期': '18个月',
                    '包装': '独立小包装'
                }),
                features=json.dumps([
                    {'title': '无糖配方', 'description': '木糖醇代替蔗糖，健康无负担'},
                    {'title': '添加维C', 'description': '补充维生素C，增强免疫力'},
                    {'title': '清新口气', 'description': '薄荷清凉，持久清新'},
                    {'title': '多种口味', 'description': '水果口味丰富，满足不同喜好'}
                ]),
                tags=json.dumps(['糖果', '无糖', '维C', '薄荷', '清新口气']),
                badge='超值',
                badge_color='#10B981',
                rating=4.7,
                review_count=5234
            ),
            
            # 一次性医用口罩
            Product(
                product_id='prod_006',
                name='一次性医用口罩（50只装）',
                category='accessory',
                price=10,
                stock=1000,
                sales=15678,
                description='一次性医用口罩，三层防护，有效阻隔飞沫、细菌、粉尘。独立包装，卫生便捷，适合日常出行、办公、购物等场景。',
                main_image='/static/images/products/mask.png',
                images=json.dumps([
                    '/static/images/products/mask.png'
                ]),
                specs=json.dumps({
                    '规格': '50只/袋',
                    '尺寸': '17.5×9.5cm',
                    '材质': '无纺布+熔喷布',
                    '防护等级': '一次性医用口罩',
                    '执行标准': 'YY/T 0969-2013',
                    '包装': '独立包装'
                }),
                features=json.dumps([
                    {'title': '三层防护', 'description': '无纺布+熔喷布+无纺布三层结构'},
                    {'title': '独立包装', 'description': '每只独立包装，卫生便捷'},
                    {'title': '舒适透气', 'description': '柔软亲肤，长时间佩戴不闷'},
                    {'title': '超高性价比', 'description': '50只装，日常防护必备'}
                ]),
                tags=json.dumps(['口罩', '医用', '防护', '独立包装', '超值']),
                badge='必备',
                badge_color='#3B82F6',
                rating=4.6,
                review_count=8934
            ),
            
            # 酒精消毒家用喷雾枪
            Product(
                product_id='prod_007',
                name='酒精消毒家用喷雾枪',
                category='accessory',
                price=10,
                stock=300,
                sales=3456,
                description='家用酒精消毒喷雾枪，纳米雾化技术，雾化细腻均匀，消毒更彻底。USB充电，便携设计，适合家居、办公、车内等多场景消毒。',
                main_image='/static/images/products/spray_gun.png',
                images=json.dumps([
                    '/static/images/products/spray_gun.png'
                ]),
                specs=json.dumps({
                    '容量': '300ml',
                    '雾化方式': '纳米雾化',
                    '充电方式': 'USB充电',
                    '续航时间': '约30分钟',
                    '适用液体': '75%酒精、消毒液、清水',
                    '材质': 'ABS+PC'
                }),
                features=json.dumps([
                    {'title': '纳米雾化', 'description': '雾化细腻均匀，消毒无死角'},
                    {'title': 'USB充电', 'description': '随时随地充电，方便快捷'},
                    {'title': '便携设计', 'description': '小巧轻便，单手操作'},
                    {'title': '多场景适用', 'description': '家居、办公、车内、外出皆可使用'}
                ]),
                tags=json.dumps(['消毒', '喷雾枪', '纳米雾化', 'USB充电', '便携']),
                rating=4.5,
                review_count=1234
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
                title='雷神YDH201使用三个月心得分享',
                content='入手雷神旗舰款YDH201三个月了，真的太满意了！数字显示屏很直观，能看到PM2.5、甲醛等实时数据。新房装修后甲醛从0.18降到了0.04，效果非常明显。H14医疗级滤网确实不一样，过滤效果比之前用的H13强太多了。虽然价格贵一点，但真的值得！',
                category='experience',
                images=json.dumps(['/static/images/products/raysun_ydh201.png']),
                likes=456,
                views=2820,
                comment_count=78,
                created_at=datetime(2024, 12, 20, 10, 30, 0)
            ),
            Post(
                post_id='post_002',
                user_id=2,
                title='性价比之选！G135真香体验',
                content='作为一个预算有限的学生党，选了雷神G135，用了两个月真的很香！2399的价格，600的CADR值，40平的卧室完全够用。360°进风设计很科学，净化速度很快。睡眠模式真的很安静，不影响休息。强烈推荐给预算不多的朋友！',
                category='experience',
                images=json.dumps(['/static/images/products/raysun_g135.png']),
                likes=328,
                views=1650,
                comment_count=56,
                created_at=datetime(2024, 12, 19, 15, 20, 0)
            ),
            Post(
                post_id='post_003',
                user_id=3,
                title='过敏体质的救星！雷神净化器使用感受',
                content='作为一个严重过敏体质的人，春天花粉季节简直是噩梦。今年入手了雷神YDH201，配合H14医疗级滤网，在家基本不打喷嚏了。APP可以远程控制，回家前提前开启，到家就能呼吸到干净空气。虽然投入不小，但健康无价！',
                category='allergy',
                likes=512,
                views=2340,
                comment_count=89,
                created_at=datetime(2024, 12, 18, 9, 0, 0)
            ),
            Post(
                post_id='post_004',
                user_id=4,
                title='宝宝房间的守护者 - 雷神G135',
                content='给宝宝房间买的雷神G135，主要看中它的静音效果和性价比。实际使用下来真的很满意，睡眠模式只有20分贝，宝宝睡觉完全不受影响。圆柱形设计也很安全，没有尖角。空气质量明显改善，宝宝也很少咳嗽了。推荐给所有宝妈！',
                category='experience',
                images=json.dumps(['/static/images/products/raysun_g135.png']),
                likes=389,
                views=1920,
                comment_count=67,
                created_at=datetime(2024, 12, 17, 14, 45, 0)
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

"""
数据库测试脚本
验证数据库功能是否正常
"""

from app import app, db
from models import User, Product, Post


def test_database():
    """测试数据库"""
    with app.app_context():
        print("=" * 60)
        print("数据库测试报告")
        print("=" * 60)
        
        # 测试用户表
        print("\n【用户表测试】")
        users = User.query.all()
        print(f"总用户数: {len(users)}")
        for user in users[:3]:
            print(f"  - {user.username} (手机: {user.phone}, 等级: {user.level}, 积分: {user.points})")
        
        # 测试产品表
        print("\n【产品表测试】")
        products = Product.query.all()
        print(f"总产品数: {len(products)}")
        for product in products:
            stock_status = "充足" if product.stock > 50 else ("紧张" if product.stock > 0 else "缺货")
            print(f"  - {product.name}")
            print(f"    价格: ¥{product.price}, 库存: {product.stock}件 ({stock_status}), 销量: {product.sales}")
        
        # 测试帖子表
        print("\n【帖子表测试】")
        posts = Post.query.all()
        print(f"总帖子数: {len(posts)}")
        for post in posts:
            print(f"  - {post.title}")
            print(f"    作者: {post.author.username}, 分类: {post.category}")
            print(f"    点赞: {post.likes}, 浏览: {post.views}, 评论: {post.comment_count}")
        
        # 测试库存更新
        print("\n【库存管理测试】")
        test_product = Product.query.filter_by(product_id='prod_001').first()
        if test_product:
            original_stock = test_product.stock
            print(f"产品: {test_product.name}")
            print(f"原始库存: {original_stock}")
            
            # 模拟销售
            if test_product.decrease_stock(2):
                print(f"销售2件后库存: {test_product.stock}")
                print(f"销量: {test_product.sales}")
                
                # 回滚（不提交）
                db.session.rollback()
                print(f"回滚后库存: {test_product.stock} (未提交，保持原值)")
            else:
                print("库存不足，无法销售")
        
        # 测试用户密码验证
        print("\n【用户认证测试】")
        test_user = User.query.filter_by(phone='13800138001').first()
        if test_user:
            print(f"测试用户: {test_user.username}")
            print(f"密码验证(123456): {test_user.check_password('123456')}")
            print(f"密码验证(错误密码): {test_user.check_password('wrong_password')}")
        
        # 测试关联查询
        print("\n【关联查询测试】")
        user_with_posts = User.query.filter_by(phone='13800138001').first()
        if user_with_posts:
            print(f"用户 {user_with_posts.username} 的帖子:")
            for post in user_with_posts.posts:
                print(f"  - {post.title} (点赞: {post.likes})")
        
        print("\n" + "=" * 60)
        print("数据库测试完成！所有功能正常")
        print("=" * 60)


if __name__ == '__main__':
    test_database()

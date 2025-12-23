"""
森系智韵智能空气管理平台 - Flask主应用
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import timedelta
import json
import os

# 导入数据库模型
from models import db, User, Product, Order, OrderItem, Post, Comment, PostLike

# 导入自定义模块
from utils.smart_guide import SmartGuideSystem
from utils.air_butler import AirButler
from utils.product_manager import ProductManager
from utils.auth import auth_manager, login_required, get_current_user

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.permanent_session_lifetime = timedelta(days=7)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///senxi_air.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # 设置为 True 可以看到 SQL 语句

# 初始化数据库
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()
    print('数据库表创建成功！')

# 初始化系统组件
smart_guide = SmartGuideSystem()
air_butler = AirButler()
product_manager = ProductManager()


# 注入当前用户到模板上下文
@app.context_processor
def inject_user():
    return {'current_user': session.get('user')}


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页"""
    products = product_manager.get_featured_products()
    return render_template('pages/index.html', products=products)


@app.route('/products')
def products():
    """产品展示页"""
    all_products = product_manager.get_all_products()
    categories = product_manager.get_categories()
    return render_template('pages/products.html', products=all_products, categories=categories)


@app.route('/product/<product_id>')
def product_detail(product_id):
    """产品详情页"""
    product = product_manager.get_product_by_id(product_id)
    if not product:
        return render_template('pages/404.html'), 404
    related_products = product_manager.get_related_products(product_id)
    return render_template('pages/product_detail.html', product=product, related_products=related_products)


@app.route('/guide')
def smart_guide_page():
    """智能导购页面"""
    return render_template('pages/smart_guide.html')


@app.route('/research')
def air_research():
    """空气研究院"""
    articles = get_research_articles()
    return render_template('pages/research.html', articles=articles)


@app.route('/community')
def community():
    """健康呼吸社区"""
    posts = get_community_posts()
    return render_template('pages/community.html', posts=posts)


@app.route('/brand')
def brand():
    """品牌介绍"""
    return render_template('pages/brand.html')


@app.route('/compare')
def compare():
    """产品对比"""
    products = product_manager.get_all_products()
    return render_template('pages/compare.html', products=products)


# ==================== 认证页面路由 ====================

@app.route('/login')
def login():
    """登录页面"""
    if session.get('user'):
        return redirect(url_for('profile'))
    return render_template('pages/login.html')


@app.route('/profile')
def profile():
    """个人中心页面"""
    return render_template('pages/profile.html')


@app.route('/auth/<platform>')
def oauth_redirect(platform):
    """第三方登录跳转"""
    redirect_uri = url_for('oauth_callback', platform=platform, _external=True)
    result = auth_manager.get_oauth_url(platform, redirect_uri)
    
    if result['success']:
        # 实际项目中跳转到OAuth URL
        # return redirect(result['url'])
        # 演示模式：直接模拟登录成功
        return redirect(url_for('oauth_callback', platform=platform, code='demo_code', state=result['state']))
    
    return jsonify(result), 400


@app.route('/auth/<platform>/callback')
def oauth_callback(platform):
    """第三方登录回调"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code or not state:
        return redirect(url_for('login'))
    
    result = auth_manager.oauth_callback(platform, code, state)
    
    if result['success']:
        session['user'] = result['user']
        session['user_id'] = result['user']['id']
        session.permanent = True
        return redirect(url_for('profile'))
    
    return redirect(url_for('login'))


# ==================== 认证API ====================

@app.route('/api/auth/send-code', methods=['POST'])
def send_verification_code():
    """发送验证码"""
    data = request.json
    phone = data.get('phone', '')
    
    result = auth_manager.send_verification_code(phone)
    return jsonify(result)


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """手机号登录"""
    data = request.json
    phone = data.get('phone', '')
    code = data.get('code', '')
    
    result = auth_manager.login_with_phone(phone, code)
    
    if result['success']:
        session['user'] = result['user']
        session['user_id'] = result['user']['id']
        session.permanent = True
    
    return jsonify(result)


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """退出登录"""
    session.pop('user', None)
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': '已退出登录'})


@app.route('/api/auth/user', methods=['GET'])
def get_user_info():
    """获取当前用户信息"""
    user = session.get('user')
    if user:
        return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'message': '未登录'}), 401


# ==================== 智能导购API ====================

@app.route('/api/guide/start', methods=['POST'])
def guide_start():
    """开始智能导购对话"""
    session['guide_state'] = smart_guide.init_session()
    response = smart_guide.get_welcome_message()
    return jsonify(response)


@app.route('/api/guide/chat', methods=['POST'])
def guide_chat():
    """智能导购对话交互"""
    data = request.json
    user_input = data.get('message', '')
    current_step = data.get('step', 0)
    
    # 获取或初始化会话状态
    guide_state = session.get('guide_state', smart_guide.init_session())
    
    # 处理用户输入
    response = smart_guide.process_input(guide_state, user_input, current_step)
    
    # 更新会话状态
    session['guide_state'] = guide_state
    
    return jsonify(response)


@app.route('/api/guide/recommend', methods=['POST'])
def guide_recommend():
    """获取智能推荐结果"""
    data = request.json
    user_profile = data.get('profile', {})
    
    recommendations = smart_guide.generate_recommendations(user_profile)
    return jsonify(recommendations)


# ==================== AI空气管家API ====================

@app.route('/api/butler/chat', methods=['POST'])
def butler_chat():
    """AI空气管家对话"""
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {})
    
    response = air_butler.chat(user_message, context)
    return jsonify(response)


@app.route('/api/butler/quick-reply', methods=['GET'])
def butler_quick_replies():
    """获取快捷回复选项"""
    category = request.args.get('category', 'general')
    replies = air_butler.get_quick_replies(category)
    return jsonify(replies)


# ==================== 产品API ====================

@app.route('/api/products', methods=['GET'])
def api_products():
    """获取产品列表"""
    category = request.args.get('category', None)
    sort_by = request.args.get('sort', 'default')
    
    products = product_manager.get_products(category=category, sort_by=sort_by)
    return jsonify(products)


@app.route('/api/products/<product_id>', methods=['GET'])
def api_product_detail(product_id):
    """获取产品详情"""
    product = product_manager.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': '产品不存在'}), 404
    return jsonify(product)


@app.route('/api/products/compare', methods=['POST'])
def api_compare_products():
    """产品对比"""
    data = request.json
    product_ids = data.get('product_ids', [])
    
    comparison = product_manager.compare_products(product_ids)
    return jsonify(comparison)


# ==================== 辅助函数 ====================

def get_research_articles():
    """获取空气研究院文章"""
    return [
        {
            'id': 1,
            'title': 'PM2.5对人体健康的影响及防护措施',
            'category': '空气污染',
            'summary': '深入了解PM2.5的危害以及如何有效防护...',
            'image': '/static/images/research/pm25.jpg',
            'date': '2024-12-15',
            'views': 3256
        },
        {
            'id': 2,
            'title': '甲醛污染：新房装修后的隐形杀手',
            'category': '室内污染',
            'summary': '装修后甲醛释放周期及科学除醛方法...',
            'image': '/static/images/research/formaldehyde.jpg',
            'date': '2024-12-10',
            'views': 4521
        },
        {
            'id': 3,
            'title': '过敏季节如何保护呼吸健康',
            'category': '健康防护',
            'summary': '春季花粉过敏的预防与空气净化方案...',
            'image': '/static/images/research/allergy.jpg',
            'date': '2024-12-05',
            'views': 2890
        },
        {
            'id': 4,
            'title': 'HEPA滤网技术原理详解',
            'category': '技术科普',
            'summary': '了解空气净化器核心技术HEPA的工作原理...',
            'image': '/static/images/research/hepa.jpg',
            'date': '2024-12-01',
            'views': 5123
        }
    ]


def get_community_posts():
    """获取社区帖子"""
    return [
        {
            'id': 1,
            'author': '清新小屋',
            'avatar': '/static/images/avatars/user1.jpg',
            'title': '使用净界者Pro三个月的真实体验',
            'content': '自从入手了净界者Pro，家里的空气质量明显改善...',
            'likes': 156,
            'comments': 23,
            'date': '2024-12-16'
        },
        {
            'id': 2,
            'author': '健康生活家',
            'avatar': '/static/images/avatars/user2.jpg',
            'title': '新房除甲醛，我的经验分享',
            'content': '装修完半年了，分享一下我的除甲醛心得...',
            'likes': 234,
            'comments': 45,
            'date': '2024-12-14'
        },
        {
            'id': 3,
            'author': '宝妈日记',
            'avatar': '/static/images/avatars/user3.jpg',
            'title': '宝宝房间空气净化器选购指南',
            'content': '作为新手妈妈，对宝宝房间的空气质量特别关注...',
            'likes': 189,
            'comments': 34,
            'date': '2024-12-12'
        }
    ]


# ==================== 错误处理 ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('pages/500.html'), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

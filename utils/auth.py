"""
用户认证模块
支持手机号登录、微信、QQ、GitHub第三方登录
"""
import hashlib
import secrets
import time
from typing import Dict, Optional
from functools import wraps
from flask import session, redirect, url_for, request


class User:
    """用户模型"""
    def __init__(self, user_id: str, nickname: str, avatar: str = None, 
                 phone: str = None, auth_type: str = 'phone'):
        self.id = user_id
        self.nickname = nickname
        self.avatar = avatar or '/static/images/default-avatar.png'
        self.phone = phone
        self.auth_type = auth_type  # phone, wechat, qq, github
        self.level = 1  # 会员等级
        self.points = 0  # 积分
        self.created_at = time.time()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'phone': self.phone,
            'auth_type': self.auth_type,
            'level': self.level,
            'points': self.points
        }


class AuthManager:
    """认证管理器"""
    
    def __init__(self):
        # 模拟用户数据库
        self.users: Dict[str, User] = {}
        # 验证码存储 {phone: (code, expire_time)}
        self.verification_codes: Dict[str, tuple] = {}
        # OAuth state存储
        self.oauth_states: Dict[str, Dict] = {}
    
    def generate_user_id(self) -> str:
        """生成用户ID"""
        return secrets.token_hex(16)
    
    def send_verification_code(self, phone: str) -> Dict:
        """发送验证码（模拟）"""
        if not self._validate_phone(phone):
            return {'success': False, 'message': '手机号格式不正确'}
        
        # 生成6位验证码
        code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        expire_time = time.time() + 300  # 5分钟有效
        
        self.verification_codes[phone] = (code, expire_time)
        
        # 实际项目中这里应调用短信API
        print(f"[DEBUG] 验证码已发送到 {phone}: {code}")
        
        return {
            'success': True, 
            'message': '验证码已发送',
            'debug_code': code  # 仅用于演示，实际项目中不返回
        }
    
    def verify_code(self, phone: str, code: str) -> bool:
        """验证验证码"""
        if phone not in self.verification_codes:
            return False
        
        stored_code, expire_time = self.verification_codes[phone]
        
        if time.time() > expire_time:
            del self.verification_codes[phone]
            return False
        
        if stored_code != code:
            return False
        
        del self.verification_codes[phone]
        return True
    
    def login_with_phone(self, phone: str, code: str) -> Dict:
        """手机号登录/注册"""
        if not self.verify_code(phone, code):
            return {'success': False, 'message': '验证码错误或已过期'}
        
        # 查找或创建用户
        user = self._find_user_by_phone(phone)
        if not user:
            user = User(
                user_id=self.generate_user_id(),
                nickname=f'用户{phone[-4:]}',
                phone=phone,
                auth_type='phone'
            )
            self.users[user.id] = user
        
        return {
            'success': True,
            'message': '登录成功',
            'user': user.to_dict()
        }
    
    def get_oauth_url(self, platform: str, redirect_uri: str) -> Dict:
        """获取第三方登录URL"""
        state = secrets.token_urlsafe(32)
        self.oauth_states[state] = {
            'platform': platform,
            'redirect_uri': redirect_uri,
            'created_at': time.time()
        }
        
        # OAuth配置（实际项目中应从环境变量读取）
        oauth_configs = {
            'wechat': {
                'auth_url': 'https://open.weixin.qq.com/connect/qrconnect',
                'app_id': 'YOUR_WECHAT_APP_ID',
                'scope': 'snsapi_login'
            },
            'qq': {
                'auth_url': 'https://graph.qq.com/oauth2.0/authorize',
                'app_id': 'YOUR_QQ_APP_ID',
                'scope': 'get_user_info'
            },
            'github': {
                'auth_url': 'https://github.com/login/oauth/authorize',
                'app_id': 'YOUR_GITHUB_CLIENT_ID',
                'scope': 'read:user'
            }
        }
        
        if platform not in oauth_configs:
            return {'success': False, 'message': '不支持的登录方式'}
        
        config = oauth_configs[platform]
        
        # 构建OAuth URL
        if platform == 'wechat':
            url = f"{config['auth_url']}?appid={config['app_id']}&redirect_uri={redirect_uri}&response_type=code&scope={config['scope']}&state={state}#wechat_redirect"
        elif platform == 'qq':
            url = f"{config['auth_url']}?response_type=code&client_id={config['app_id']}&redirect_uri={redirect_uri}&state={state}&scope={config['scope']}"
        elif platform == 'github':
            url = f"{config['auth_url']}?client_id={config['app_id']}&redirect_uri={redirect_uri}&state={state}&scope={config['scope']}"
        
        return {
            'success': True,
            'url': url,
            'state': state,
            'platform': platform
        }
    
    def oauth_callback(self, platform: str, code: str, state: str) -> Dict:
        """OAuth回调处理"""
        # 验证state
        if state not in self.oauth_states:
            return {'success': False, 'message': '无效的认证请求'}
        
        oauth_info = self.oauth_states[state]
        if oauth_info['platform'] != platform:
            return {'success': False, 'message': '认证平台不匹配'}
        
        # 清理state
        del self.oauth_states[state]
        
        # 模拟获取用户信息（实际项目中应调用对应平台API）
        mock_user_info = self._mock_oauth_user_info(platform, code)
        
        # 查找或创建用户
        oauth_id = f"{platform}_{mock_user_info['openid']}"
        user = self.users.get(oauth_id)
        
        if not user:
            user = User(
                user_id=oauth_id,
                nickname=mock_user_info['nickname'],
                avatar=mock_user_info['avatar'],
                auth_type=platform
            )
            self.users[user.id] = user
        
        return {
            'success': True,
            'message': '登录成功',
            'user': user.to_dict()
        }
    
    def _mock_oauth_user_info(self, platform: str, code: str) -> Dict:
        """模拟获取OAuth用户信息"""
        avatars = {
            'wechat': 'https://thirdwx.qlogo.cn/mmopen/vi_32/default/0',
            'qq': 'https://q.qlogo.cn/headimg_dl?dst_uin=10000&spec=640',
            'github': 'https://avatars.githubusercontent.com/u/0'
        }
        
        return {
            'openid': hashlib.md5(code.encode()).hexdigest()[:16],
            'nickname': f'{platform.title()}用户',
            'avatar': avatars.get(platform, '')
        }
    
    def _find_user_by_phone(self, phone: str) -> Optional[User]:
        """根据手机号查找用户"""
        for user in self.users.values():
            if user.phone == phone:
                return user
        return None
    
    def _validate_phone(self, phone: str) -> bool:
        """验证手机号格式"""
        if not phone or len(phone) != 11:
            return False
        return phone.isdigit() and phone[0] == '1'
    
    def get_current_user(self) -> Optional[User]:
        """获取当前登录用户"""
        user_id = session.get('user_id')
        if user_id and user_id in self.users:
            return self.users[user_id]
        return None
    
    def login_user(self, user: User):
        """登录用户（设置session）"""
        session['user_id'] = user.id
        session['user'] = user.to_dict()
        session.permanent = True
    
    def logout_user(self):
        """登出用户"""
        session.pop('user_id', None)
        session.pop('user', None)


# 全局认证管理器实例
auth_manager = AuthManager()


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_manager.get_current_user():
            if request.is_json:
                return {'success': False, 'message': '请先登录'}, 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """获取当前用户（供模板使用）"""
    return auth_manager.get_current_user()

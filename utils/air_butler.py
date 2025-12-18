"""
AI空气管家 - 智能客服系统
森系智韵智能空气管理平台核心模块
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class AirButler:
    """
    AI空气管家
    提供全天候在线响应，覆盖产品咨询、使用指导、故障排查等服务
    """
    
    # 意图识别关键词
    INTENT_KEYWORDS = {
        'product_inquiry': ['推荐', '哪款', '选择', '对比', '区别', '哪个好', '买什么', '适合'],
        'usage_guide': ['怎么用', '如何使用', '操作', '设置', '连接', '配对', 'APP', '模式'],
        'troubleshoot': ['故障', '问题', '不工作', '坏了', '异常', '噪音大', '不转', '报警', '闪烁'],
        'filter_replace': ['滤芯', '滤网', '更换', '清洗', '多久换', '寿命', '耗材'],
        'air_quality': ['空气质量', 'PM2.5', '甲醛', 'AQI', '污染', '指数', '数值'],
        'order_service': ['订单', '物流', '发货', '退货', '换货', '售后', '保修'],
        'general': ['你好', '在吗', '帮助', '客服', '人工']
    }
    
    # 快捷回复模板
    QUICK_REPLIES = {
        'general': [
            '如何选择适合我的空气净化器？',
            '净界者产品有什么特点？',
            '滤芯多久需要更换？',
            '如何查看空气质量数据？'
        ],
        'product': [
            '森林呼吸Pro和清新之风Max有什么区别？',
            '哪款适合婴儿房使用？',
            '除甲醛效果最好的是哪款？',
            '有没有适合大客厅的产品？'
        ],
        'usage': [
            '如何连接手机APP？',
            '睡眠模式怎么开启？',
            '自动模式是如何工作的？',
            '如何设置定时开关机？'
        ],
        'troubleshoot': [
            '净化器噪音变大怎么办？',
            '显示屏一直闪烁是什么原因？',
            '出风口风量变小了怎么处理？',
            '滤芯指示灯亮了怎么办？'
        ]
    }
    
    # 知识库
    KNOWLEDGE_BASE = {
        # 产品知识
        'products': {
            'mini': {
                'name': '自然守护Mini',
                'features': 'HEPA H12滤网，CADR值200m³/h，适用14-24㎡，静音模式仅25dB',
                'suitable': '小卧室、书房、办公桌',
                'price': '1299元'
            },
            'pro': {
                'name': '森林呼吸Pro',
                'features': 'HEPA H13滤网，CADR值450m³/h，甲醛CADR 200m³/h，智能感应，APP控制',
                'suitable': '客厅、卧室、办公室',
                'price': '2999元'
            },
            'max': {
                'name': '清新之风Max',
                'features': 'HEPA H13+双重活性炭，CADR值800m³/h，UV消毒，负离子，甲醛数显',
                'suitable': '大客厅、全屋、别墅',
                'price': '5999元'
            },
            'uv': {
                'name': '紫光卫士',
                'features': 'HEPA H13+UV-C消毒，等离子杀菌，医疗级认证',
                'suitable': '婴儿房、老人房、病患房间',
                'price': '3999元'
            }
        },
        
        # 使用指南
        'usage_guides': {
            'app_connect': '''
连接手机APP步骤：
1. 下载"净界者"APP（iOS/Android均可）
2. 注册并登录账号
3. 确保手机连接2.4GHz WiFi
4. 点击APP首页"+"添加设备
5. 长按净化器WiFi键3秒进入配网模式
6. 按APP提示完成配对
            ''',
            'sleep_mode': '''
睡眠模式开启方法：
1. 按下机身"模式"按钮切换至睡眠模式
2. 或在APP中选择"睡眠模式"
睡眠模式特点：
- 风速自动降至最低档
- 显示屏亮度降低或关闭
- 噪音低至25dB
- 自动感应空气质量调节
            ''',
            'auto_mode': '''
自动模式工作原理：
净化器内置高精度空气质量传感器，实时监测：
- PM2.5浓度
- VOC/甲醛浓度
- 温湿度
根据监测数据自动调节风速：
- 空气优良：低速静音运行
- 轻度污染：中速净化
- 重度污染：高速强力净化
            '''
        },
        
        # 故障排查
        'troubleshooting': {
            'noise': '''
噪音变大可能原因及解决方案：
1. 滤芯堵塞 → 检查并更换滤芯
2. 进风口被遮挡 → 确保四周留有足够空间
3. 风扇积灰 → 用软刷清洁风扇叶片
4. 机器未放平 → 调整至水平位置
5. 内部异物 → 关机检查是否有异物进入
如问题持续，请联系售后服务。
            ''',
            'display_flash': '''
显示屏闪烁原因：
1. 滤芯寿命到期提醒 → 更换新滤芯后重置
2. 传感器需要清洁 → 用棉签轻轻清洁传感器
3. 电源电压不稳 → 更换稳定电源插座
4. 系统故障 → 长按电源键10秒重启
            ''',
            'weak_airflow': '''
出风量变小解决方案：
1. 首先检查滤芯是否需要更换
2. 清洁进风口和出风口
3. 检查是否误开启睡眠/静音模式
4. 确认风速档位设置
5. 检查滤芯安装是否正确
            ''',
            'filter_indicator': '''
滤芯指示灯亮起说明：
滤芯已达到建议更换时间，请及时更换以保证净化效果。
更换步骤：
1. 关闭并断开电源
2. 打开后盖/侧盖
3. 取出旧滤芯
4. 装入新滤芯（注意方向）
5. 盖好盖板
6. 开机后长按滤芯重置键3秒
            '''
        },
        
        # 滤芯知识
        'filter_info': {
            'lifespan': '建议6-12个月更换一次，具体取决于使用环境和频率。重污染地区或24小时运行建议6个月更换。',
            'types': {
                'hepa': 'HEPA滤网：过滤PM2.5、花粉、灰尘等颗粒物，不可水洗',
                'carbon': '活性炭滤网：吸附甲醛、异味、VOC，不可水洗',
                'pre': '初效滤网：过滤大颗粒灰尘毛发，可定期清洗'
            },
            'purchase': '请通过官方渠道购买原装滤芯，确保净化效果和安全性。'
        },
        
        # 空气质量知识
        'air_quality': {
            'aqi_levels': {
                '0-50': '优，空气质量令人满意，基本无污染',
                '51-100': '良，空气质量可接受，敏感人群应减少户外活动',
                '101-150': '轻度污染，敏感人群会有不适',
                '151-200': '中度污染，进一步加剧敏感人群症状',
                '201-300': '重度污染，所有人都可能受到影响',
                '300+': '严重污染，健康警报，所有人应避免户外活动'
            },
            'pm25': 'PM2.5是直径小于2.5微米的细颗粒物，可深入肺部甚至血液，WHO建议年均值不超过5μg/m³',
            'formaldehyde': '甲醛是一类致癌物，室内安全标准为≤0.08mg/m³，新装修房屋甲醛释放周期可达3-15年'
        }
    }
    
    def __init__(self):
        """初始化AI空气管家"""
        self.conversation_history = []
    
    def chat(self, user_message: str, context: Dict = None) -> Dict:
        """
        处理用户消息并返回回复
        
        Args:
            user_message: 用户输入的消息
            context: 上下文信息（设备信息、历史记录等）
        
        Returns:
            回复消息字典
        """
        # 识别用户意图
        intent = self._identify_intent(user_message)
        
        # 根据意图生成回复
        response = self._generate_response(intent, user_message, context)
        
        # 记录对话历史
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': response['message'],
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _identify_intent(self, message: str) -> str:
        """识别用户意图"""
        message_lower = message.lower()
        
        intent_scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return 'general'
    
    def _generate_response(self, intent: str, message: str, context: Dict = None) -> Dict:
        """根据意图生成回复"""
        
        if intent == 'product_inquiry':
            return self._handle_product_inquiry(message)
        elif intent == 'usage_guide':
            return self._handle_usage_guide(message)
        elif intent == 'troubleshoot':
            return self._handle_troubleshoot(message)
        elif intent == 'filter_replace':
            return self._handle_filter_inquiry(message)
        elif intent == 'air_quality':
            return self._handle_air_quality(message)
        elif intent == 'order_service':
            return self._handle_order_service(message)
        else:
            return self._handle_general(message)
    
    def _handle_product_inquiry(self, message: str) -> Dict:
        """处理产品咨询"""
        message_lower = message.lower()
        
        # 检查是否询问特定产品
        if 'mini' in message_lower or '入门' in message_lower or '便宜' in message_lower:
            product = self.KNOWLEDGE_BASE['products']['mini']
            response_text = f"推荐您了解我们的{product['name']}：\n\n{product['features']}\n\n适用场景：{product['suitable']}\n价格：{product['price']}\n\n这款产品性价比很高，非常适合小空间使用。"
        
        elif 'pro' in message_lower or '除甲醛' in message_lower or '智能' in message_lower:
            product = self.KNOWLEDGE_BASE['products']['pro']
            response_text = f"为您推荐{product['name']}：\n\n{product['features']}\n\n适用场景：{product['suitable']}\n价格：{product['price']}\n\n这是我们的明星产品，除甲醛效果出色，支持智能控制。"
        
        elif 'max' in message_lower or '大' in message_lower or '全屋' in message_lower or '旗舰' in message_lower:
            product = self.KNOWLEDGE_BASE['products']['max']
            response_text = f"隆重推荐{product['name']}：\n\n{product['features']}\n\n适用场景：{product['suitable']}\n价格：{product['price']}\n\n这是我们的旗舰产品，适合大空间和追求极致净化效果的用户。"
        
        elif '婴儿' in message_lower or '宝宝' in message_lower or '杀菌' in message_lower or '消毒' in message_lower:
            product = self.KNOWLEDGE_BASE['products']['uv']
            response_text = f"特别推荐{product['name']}：\n\n{product['features']}\n\n适用场景：{product['suitable']}\n价格：{product['price']}\n\n这款产品通过医疗级认证，UV-C消毒功能可有效杀灭细菌病毒，特别适合有婴幼儿或免疫力较弱人群的家庭。"
        
        else:
            response_text = """我来帮您选择合适的产品！我们有以下系列：

🌿 **自然守护Mini** (¥1299)
适合小空间，静音设计，入门首选

🌲 **森林呼吸Pro** (¥2999) ⭐销量冠军
除甲醛专家，智能控制，适合大多数家庭

🍃 **清新之风Max** (¥5999)
旗舰之选，全能净化，适合大空间

💜 **紫光卫士** (¥3999)
医疗级杀菌，母婴优选

您可以告诉我您的具体需求（房间大小、主要问题、预算等），我来为您精准推荐！"""
        
        return {
            'message': response_text,
            'intent': 'product_inquiry',
            'quick_replies': self.QUICK_REPLIES['product'],
            'show_products': True
        }
    
    def _handle_usage_guide(self, message: str) -> Dict:
        """处理使用指南"""
        message_lower = message.lower()
        
        if 'app' in message_lower or '连接' in message_lower or '配对' in message_lower:
            response_text = self.KNOWLEDGE_BASE['usage_guides']['app_connect']
        elif '睡眠' in message_lower:
            response_text = self.KNOWLEDGE_BASE['usage_guides']['sleep_mode']
        elif '自动' in message_lower:
            response_text = self.KNOWLEDGE_BASE['usage_guides']['auto_mode']
        else:
            response_text = """我可以帮您解答使用问题，请问您想了解：

1. 📱 如何连接手机APP
2. 🌙 睡眠模式使用方法
3. 🔄 自动模式工作原理
4. ⏰ 定时功能设置
5. 🔧 滤芯更换方法

请选择或直接描述您的问题。"""
        
        return {
            'message': response_text,
            'intent': 'usage_guide',
            'quick_replies': self.QUICK_REPLIES['usage']
        }
    
    def _handle_troubleshoot(self, message: str) -> Dict:
        """处理故障排查"""
        message_lower = message.lower()
        
        if '噪音' in message_lower or '声音大' in message_lower:
            response_text = self.KNOWLEDGE_BASE['troubleshooting']['noise']
        elif '闪烁' in message_lower or '显示' in message_lower:
            response_text = self.KNOWLEDGE_BASE['troubleshooting']['display_flash']
        elif '风' in message_lower and ('小' in message_lower or '弱' in message_lower):
            response_text = self.KNOWLEDGE_BASE['troubleshooting']['weak_airflow']
        elif '滤芯' in message_lower and ('灯' in message_lower or '亮' in message_lower):
            response_text = self.KNOWLEDGE_BASE['troubleshooting']['filter_indicator']
        else:
            response_text = """我来帮您排查问题。常见故障及解决方案：

🔊 **噪音变大** - 可能是滤芯堵塞或风扇积灰
💡 **显示屏闪烁** - 可能是滤芯提醒或传感器需清洁
💨 **出风量变小** - 检查滤芯和运行模式
⚠️ **滤芯指示灯亮** - 需要更换滤芯

请描述具体症状，我来为您提供针对性解决方案。

如果问题无法解决，可以转接人工客服为您服务。"""
        
        return {
            'message': response_text,
            'intent': 'troubleshoot',
            'quick_replies': self.QUICK_REPLIES['troubleshoot'],
            'show_human_service': True
        }
    
    def _handle_filter_inquiry(self, message: str) -> Dict:
        """处理滤芯相关咨询"""
        message_lower = message.lower()
        
        if '多久' in message_lower or '寿命' in message_lower or '更换' in message_lower:
            response_text = f"**滤芯更换周期**\n\n{self.KNOWLEDGE_BASE['filter_info']['lifespan']}\n\n**滤芯类型说明：**\n"
            for filter_type, desc in self.KNOWLEDGE_BASE['filter_info']['types'].items():
                response_text += f"• {desc}\n"
            response_text += f"\n{self.KNOWLEDGE_BASE['filter_info']['purchase']}"
        else:
            response_text = """**滤芯知识小课堂**

🔹 **HEPA滤网**
过滤PM2.5、花粉、灰尘等，建议6-12个月更换

🔹 **活性炭滤网**
吸附甲醛、异味、VOC，建议6-12个月更换

🔹 **初效滤网**
过滤大颗粒物，可定期清洗重复使用

**温馨提示：**
• 重污染地区建议缩短更换周期
• 请购买官方原装滤芯
• 更换后记得重置滤芯计时器"""
        
        return {
            'message': response_text,
            'intent': 'filter_replace',
            'quick_replies': ['如何购买原装滤芯？', '滤芯更换步骤', '如何重置滤芯计时器？']
        }
    
    def _handle_air_quality(self, message: str) -> Dict:
        """处理空气质量咨询"""
        message_lower = message.lower()
        
        if 'aqi' in message_lower or '指数' in message_lower:
            response_text = "**空气质量指数(AQI)等级说明：**\n\n"
            for level, desc in self.KNOWLEDGE_BASE['air_quality']['aqi_levels'].items():
                response_text += f"• AQI {level}：{desc}\n"
        elif 'pm2.5' in message_lower or 'pm' in message_lower:
            response_text = f"**PM2.5知识**\n\n{self.KNOWLEDGE_BASE['air_quality']['pm25']}\n\n净界者空气净化器采用HEPA H13滤网，对PM2.5过滤效率达99.97%。"
        elif '甲醛' in message_lower:
            response_text = f"**甲醛知识**\n\n{self.KNOWLEDGE_BASE['air_quality']['formaldehyde']}\n\n推荐使用森林呼吸Pro或清新之风Max，配备专业除醛滤网和甲醛数显功能。"
        else:
            response_text = """**空气质量小百科**

🌡️ **常见空气污染物：**
• PM2.5 - 细颗粒物，可深入肺部
• 甲醛 - 装修污染主要来源
• VOC - 挥发性有机化合物
• 花粉 - 季节性过敏原

📊 **AQI空气质量指数：**
0-50 优 | 51-100 良 | 101-150 轻度污染
151-200 中度 | 201-300 重度 | 300+ 严重

您想了解哪方面的详细信息？"""
        
        return {
            'message': response_text,
            'intent': 'air_quality',
            'quick_replies': ['什么是PM2.5？', '甲醛危害有哪些？', 'AQI指数怎么看？']
        }
    
    def _handle_order_service(self, message: str) -> Dict:
        """处理订单服务"""
        response_text = """**订单与售后服务**

📦 **物流查询**
请登录APP或官网，在"我的订单"中查看物流信息

🔄 **退换货政策**
• 7天无理由退货
• 15天换货
• 1年整机保修
• 核心部件3年保修

📞 **联系方式**
• 客服热线：400-888-8888
• 服务时间：9:00-21:00
• 在线客服：APP内咨询

如需人工服务，请点击下方按钮转接。"""
        
        return {
            'message': response_text,
            'intent': 'order_service',
            'quick_replies': ['查询订单状态', '申请退换货', '联系人工客服'],
            'show_human_service': True
        }
    
    def _handle_general(self, message: str) -> Dict:
        """处理通用问题"""
        response_text = """您好！我是森系智韵的AI空气管家 🌿

我可以帮您：
• 🛒 **产品推荐** - 根据需求推荐合适的空气净化器
• 📖 **使用指导** - 解答产品使用问题
• 🔧 **故障排查** - 帮您解决设备问题
• 🔄 **滤芯服务** - 滤芯更换指导
• 🌡️ **空气知识** - 空气质量科普

请问有什么可以帮您的？"""
        
        return {
            'message': response_text,
            'intent': 'general',
            'quick_replies': self.QUICK_REPLIES['general']
        }
    
    def get_quick_replies(self, category: str = 'general') -> List[str]:
        """获取快捷回复选项"""
        return self.QUICK_REPLIES.get(category, self.QUICK_REPLIES['general'])
    
    def transfer_to_human(self, context: Dict = None) -> Dict:
        """转接人工客服"""
        return {
            'message': '正在为您转接人工客服，请稍候...\n\n当前排队人数：2人\n预计等待时间：约3分钟\n\n您也可以留下联系方式，客服将在工作时间内回电。',
            'intent': 'transfer',
            'transfer_status': 'pending',
            'queue_position': 2
        }

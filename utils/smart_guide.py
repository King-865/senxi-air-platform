"""
智能导购系统 - 多轮对话流程实现
森系智韵智能空气管理平台核心模块
"""
import json
from typing import Dict, List, Any, Optional


class SmartGuideSystem:
    """
    智能导购系统
    通过多轮对话引导用户输入需求信息，智能生成空气管理解决方案
    """
    
    # 对话流程步骤定义
    STEPS = {
        0: 'welcome',           # 欢迎语
        1: 'area',              # 房屋面积
        2: 'region',            # 居住区域
        3: 'problems',          # 主要空气问题
        4: 'users',             # 使用人群
        5: 'space_type',        # 空间类型
        6: 'budget',            # 预算范围
        7: 'recommendation'     # 推荐结果
    }
    
    # 区域空气特征数据
    REGION_CHARACTERISTICS = {
        'north': {
            'name': '北方地区',
            'features': ['冬季供暖期PM2.5较高', '春季沙尘天气', '室内干燥'],
            'recommended_features': ['高效PM2.5过滤', '加湿功能', '大风量']
        },
        'south': {
            'name': '南方地区', 
            'features': ['湿度较高', '梅雨季节霉菌滋生', '夏季高温'],
            'recommended_features': ['除湿功能', '抗菌过滤', '静音设计']
        },
        'coastal': {
            'name': '沿海地区',
            'features': ['空气湿度大', '盐分腐蚀', '台风季节'],
            'recommended_features': ['防潮设计', '耐腐蚀材质', '除湿功能']
        },
        'inland': {
            'name': '内陆地区',
            'features': ['气候干燥', '温差较大', '扬尘较多'],
            'recommended_features': ['加湿功能', '高效除尘', '智能温控']
        },
        'industrial': {
            'name': '工业区附近',
            'features': ['工业废气', 'VOC污染', '粉尘较多'],
            'recommended_features': ['活性炭滤网', 'VOC过滤', '高CADR值']
        }
    }
    
    # 空气问题类型
    AIR_PROBLEMS = {
        'pm25': {'name': 'PM2.5/雾霾', 'weight': 1.2, 'solution': 'HEPA H13高效过滤'},
        'formaldehyde': {'name': '甲醛/装修污染', 'weight': 1.3, 'solution': '活性炭+光触媒分解'},
        'allergen': {'name': '过敏原/花粉', 'weight': 1.1, 'solution': '多层过滤+负离子'},
        'bacteria': {'name': '细菌/病毒', 'weight': 1.4, 'solution': 'UV紫外线消毒'},
        'odor': {'name': '异味/烟味', 'weight': 1.0, 'solution': '活性炭吸附'},
        'dust': {'name': '灰尘/毛发', 'weight': 0.9, 'solution': '初效+HEPA过滤'}
    }
    
    # 使用人群特征
    USER_GROUPS = {
        'baby': {'name': '婴幼儿', 'priority': ['静音', '无臭氧', '高安全性'], 'weight': 1.5},
        'elderly': {'name': '老年人', 'priority': ['操作简单', '低噪音', '大显示屏'], 'weight': 1.3},
        'pregnant': {'name': '孕妇', 'priority': ['零臭氧', '低辐射', '高效净化'], 'weight': 1.4},
        'allergy': {'name': '过敏人群', 'priority': ['HEPA过滤', '负离子', '花粉模式'], 'weight': 1.3},
        'respiratory': {'name': '呼吸道疾病患者', 'priority': ['医疗级过滤', '静音', '24小时运行'], 'weight': 1.4},
        'pet': {'name': '宠物家庭', 'priority': ['除毛发', '除异味', '大风量'], 'weight': 1.1},
        'general': {'name': '普通成人', 'priority': ['性价比', '智能控制', '节能'], 'weight': 1.0}
    }
    
    # 空间类型
    SPACE_TYPES = {
        'bedroom': {'name': '卧室', 'features': ['静音优先', '夜间模式', '小巧设计']},
        'living': {'name': '客厅', 'features': ['大风量', '快速净化', '美观设计']},
        'nursery': {'name': '婴儿房', 'features': ['超静音', '安全锁', '无臭氧']},
        'office': {'name': '办公室', 'features': ['长时间运行', '低能耗', '智能控制']},
        'whole_house': {'name': '全屋', 'features': ['超大CADR', '多房间覆盖', '中央控制']}
    }
    
    # 预算范围
    BUDGET_RANGES = {
        'economy': {'name': '经济型', 'range': '1000-2000元', 'min': 1000, 'max': 2000},
        'standard': {'name': '标准型', 'range': '2000-4000元', 'min': 2000, 'max': 4000},
        'premium': {'name': '高端型', 'range': '4000-8000元', 'min': 4000, 'max': 8000},
        'luxury': {'name': '旗舰型', 'range': '8000元以上', 'min': 8000, 'max': 50000}
    }
    
    def __init__(self):
        """初始化智能导购系统"""
        self.products = self._load_products()
    
    def _load_products(self) -> List[Dict]:
        """加载产品数据"""
        # 产品数据库
        return [
            {
                'id': 'mini-01',
                'name': '净界者·自然守护Mini',
                'series': '自然守护',
                'price': 1299,
                'original_price': 1599,
                'cadr': 200,
                'applicable_area': '14-24㎡',
                'noise': '25-48dB',
                'features': ['HEPA H12', '初效滤网', '三档风速', '静音模式'],
                'suitable_for': ['bedroom', 'nursery', 'office'],
                'problems': ['pm25', 'dust', 'allergen'],
                'user_groups': ['general', 'baby'],
                'image': '/static/images/products/mini.png',
                'rating': 4.7,
                'reviews': 2356,
                'tags': ['入门首选', '静音设计', '高性价比']
            },
            {
                'id': 'pro-01',
                'name': '净界者·森林呼吸Pro',
                'series': '森林呼吸',
                'price': 2999,
                'original_price': 3599,
                'cadr': 450,
                'applicable_area': '31-54㎡',
                'noise': '28-55dB',
                'features': ['HEPA H13', '活性炭滤网', '甲醛分解', '智能感应', 'APP控制'],
                'suitable_for': ['living', 'bedroom', 'office'],
                'problems': ['pm25', 'formaldehyde', 'odor', 'allergen'],
                'user_groups': ['general', 'allergy', 'pet'],
                'image': '/static/images/products/pro.png',
                'rating': 4.8,
                'reviews': 5621,
                'tags': ['销量冠军', '除醛专家', '智能互联']
            },
            {
                'id': 'max-01',
                'name': '净界者·清新之风Max',
                'series': '清新之风',
                'price': 5999,
                'original_price': 7299,
                'cadr': 800,
                'applicable_area': '56-96㎡',
                'noise': '30-58dB',
                'features': ['HEPA H13', '双重活性炭', 'UV消毒', '负离子', '甲醛数显', '全屋互联'],
                'suitable_for': ['living', 'whole_house'],
                'problems': ['pm25', 'formaldehyde', 'bacteria', 'odor', 'allergen', 'dust'],
                'user_groups': ['general', 'baby', 'elderly', 'pregnant', 'respiratory'],
                'image': '/static/images/products/max.png',
                'rating': 4.9,
                'reviews': 3892,
                'tags': ['旗舰之选', '全能净化', '医疗级']
            },
            {
                'id': 'uv-01',
                'name': '净界者·紫光卫士',
                'series': '紫光卫士',
                'price': 3999,
                'original_price': 4599,
                'cadr': 380,
                'applicable_area': '26-46㎡',
                'noise': '26-52dB',
                'features': ['HEPA H13', 'UV-C消毒', '等离子杀菌', '病毒过滤', '医疗认证'],
                'suitable_for': ['nursery', 'bedroom', 'office'],
                'problems': ['bacteria', 'pm25', 'allergen'],
                'user_groups': ['baby', 'elderly', 'pregnant', 'respiratory'],
                'image': '/static/images/products/uv.png',
                'rating': 4.8,
                'reviews': 1876,
                'tags': ['杀菌专家', '母婴优选', '医疗级']
            },
            {
                'id': 'car-01',
                'name': '净界者·车载清风',
                'series': '车载系列',
                'price': 699,
                'original_price': 899,
                'cadr': 30,
                'applicable_area': '车内空间',
                'noise': '≤35dB',
                'features': ['HEPA H11', '活性炭', '负离子', 'USB供电', '便携设计'],
                'suitable_for': ['car'],
                'problems': ['odor', 'pm25', 'formaldehyde'],
                'user_groups': ['general'],
                'image': '/static/images/products/car.png',
                'rating': 4.6,
                'reviews': 4521,
                'tags': ['车载必备', '新车除味', '便携小巧']
            }
        ]
    
    def init_session(self) -> Dict:
        """初始化会话状态"""
        return {
            'current_step': 0,
            'user_profile': {
                'area': None,
                'region': None,
                'problems': [],
                'users': [],
                'space_type': None,
                'budget': None
            },
            'conversation_history': []
        }
    
    def get_welcome_message(self) -> Dict:
        """获取欢迎消息"""
        return {
            'step': 0,
            'type': 'welcome',
            'message': '您好！我是森系智韵的智能空气顾问。接下来我将通过几个简单的问题，为您量身定制专属的空气管理方案。准备好了吗？',
            'next_step': 1,
            'options': None,
            'progress': 0
        }
    
    def process_input(self, state: Dict, user_input: str, step: int) -> Dict:
        """处理用户输入并返回下一步对话"""
        
        # 根据当前步骤处理输入
        if step == 1:
            return self._process_area(state, user_input)
        elif step == 2:
            return self._process_region(state, user_input)
        elif step == 3:
            return self._process_problems(state, user_input)
        elif step == 4:
            return self._process_users(state, user_input)
        elif step == 5:
            return self._process_space_type(state, user_input)
        elif step == 6:
            return self._process_budget(state, user_input)
        else:
            return self.get_welcome_message()
    
    def _process_area(self, state: Dict, user_input: str) -> Dict:
        """处理房屋面积输入"""
        try:
            area = int(user_input)
            state['user_profile']['area'] = area
        except ValueError:
            # 尝试从文本中提取数字
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                area = int(numbers[0])
                state['user_profile']['area'] = area
            else:
                return {
                    'step': 1,
                    'type': 'area',
                    'message': '抱歉，我没有理解您输入的面积。请输入一个数字，例如：30',
                    'next_step': 1,
                    'options': self._get_area_options(),
                    'progress': 14
                }
        
        return {
            'step': 2,
            'type': 'region',
            'message': f'好的，您的空间面积是{state["user_profile"]["area"]}平方米。请问您居住在哪个区域？不同区域的空气特征会影响我们的推荐方案。',
            'next_step': 2,
            'options': self._get_region_options(),
            'progress': 28
        }
    
    def _process_region(self, state: Dict, user_input: str) -> Dict:
        """处理居住区域输入"""
        region_key = self._match_region(user_input)
        state['user_profile']['region'] = region_key
        
        region_info = self.REGION_CHARACTERISTICS.get(region_key, {})
        features_text = '、'.join(region_info.get('features', [])[:2])
        
        return {
            'step': 3,
            'type': 'problems',
            'message': f'了解了，{region_info.get("name", "您所在的区域")}的空气特点是：{features_text}。请问您最关注哪些空气问题？（可多选）',
            'next_step': 3,
            'options': self._get_problems_options(),
            'progress': 42,
            'multi_select': True
        }
    
    def _process_problems(self, state: Dict, user_input: str) -> Dict:
        """处理空气问题输入"""
        problems = self._parse_multi_select(user_input, self.AIR_PROBLEMS)
        state['user_profile']['problems'] = problems if problems else ['pm25']
        
        problems_text = '、'.join([self.AIR_PROBLEMS[p]['name'] for p in state['user_profile']['problems']])
        
        return {
            'step': 4,
            'type': 'users',
            'message': f'明白了，您主要关注{problems_text}问题。请问家中主要有哪些成员？（可多选，这将帮助我们推荐更适合的产品）',
            'next_step': 4,
            'options': self._get_users_options(),
            'progress': 56,
            'multi_select': True
        }
    
    def _process_users(self, state: Dict, user_input: str) -> Dict:
        """处理使用人群输入"""
        users = self._parse_multi_select(user_input, self.USER_GROUPS)
        state['user_profile']['users'] = users if users else ['general']
        
        return {
            'step': 5,
            'type': 'space_type',
            'message': '请问您主要想在哪个空间使用空气净化器？',
            'next_step': 5,
            'options': self._get_space_options(),
            'progress': 70
        }
    
    def _process_space_type(self, state: Dict, user_input: str) -> Dict:
        """处理空间类型输入"""
        space_key = self._match_space(user_input)
        state['user_profile']['space_type'] = space_key
        
        return {
            'step': 6,
            'type': 'budget',
            'message': '最后一个问题，请问您的预算范围是？',
            'next_step': 6,
            'options': self._get_budget_options(),
            'progress': 84
        }
    
    def _process_budget(self, state: Dict, user_input: str) -> Dict:
        """处理预算输入并生成推荐"""
        budget_key = self._match_budget(user_input)
        state['user_profile']['budget'] = budget_key
        
        # 生成推荐结果
        recommendations = self.generate_recommendations(state['user_profile'])
        
        return {
            'step': 7,
            'type': 'recommendation',
            'message': '感谢您的耐心回答！根据您的需求，我为您精心挑选了以下空气管理方案：',
            'next_step': 7,
            'recommendations': recommendations,
            'progress': 100,
            'user_profile_summary': self._generate_profile_summary(state['user_profile'])
        }
    
    def generate_recommendations(self, profile: Dict) -> List[Dict]:
        """根据用户画像生成产品推荐"""
        scored_products = []
        
        for product in self.products:
            score = self._calculate_match_score(product, profile)
            if score > 0:
                scored_products.append({
                    'product': product,
                    'score': score,
                    'match_reasons': self._get_match_reasons(product, profile)
                })
        
        # 按匹配度排序
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        
        # 返回前3个推荐
        return scored_products[:3]
    
    def _calculate_match_score(self, product: Dict, profile: Dict) -> float:
        """计算产品与用户需求的匹配分数"""
        score = 50  # 基础分
        
        # 面积匹配
        if profile.get('area'):
            area = profile['area']
            # 解析产品适用面积
            applicable = product.get('applicable_area', '0-0')
            if '-' in applicable:
                try:
                    min_area, max_area = map(lambda x: int(x.replace('㎡', '')), applicable.split('-'))
                    if min_area <= area <= max_area:
                        score += 20
                    elif area < min_area:
                        score += 10  # 面积小于推荐范围，仍可使用
                    else:
                        score -= 10  # 面积超出推荐范围
                except:
                    pass
        
        # 空气问题匹配
        user_problems = set(profile.get('problems', []))
        product_problems = set(product.get('problems', []))
        problem_match = len(user_problems & product_problems)
        score += problem_match * 10
        
        # 使用人群匹配
        user_groups = set(profile.get('users', []))
        product_groups = set(product.get('user_groups', []))
        group_match = len(user_groups & product_groups)
        score += group_match * 8
        
        # 特殊人群加权
        special_groups = {'baby', 'elderly', 'pregnant', 'respiratory'}
        if user_groups & special_groups:
            if product_groups & special_groups:
                score += 15
        
        # 空间类型匹配
        if profile.get('space_type') in product.get('suitable_for', []):
            score += 15
        
        # 预算匹配
        budget = profile.get('budget')
        if budget:
            budget_range = self.BUDGET_RANGES.get(budget, {})
            price = product.get('price', 0)
            if budget_range.get('min', 0) <= price <= budget_range.get('max', 999999):
                score += 20
            elif price < budget_range.get('min', 0):
                score += 10  # 低于预算也可接受
            else:
                score -= 15  # 超出预算扣分
        
        return min(score, 100)  # 最高100分
    
    def _get_match_reasons(self, product: Dict, profile: Dict) -> List[str]:
        """获取匹配原因说明"""
        reasons = []
        
        # 面积匹配说明
        if profile.get('area'):
            reasons.append(f"适用面积覆盖您的{profile['area']}㎡空间")
        
        # 问题解决说明
        user_problems = set(profile.get('problems', []))
        product_problems = set(product.get('problems', []))
        matched_problems = user_problems & product_problems
        if matched_problems:
            problem_names = [self.AIR_PROBLEMS[p]['name'] for p in matched_problems]
            reasons.append(f"有效解决{'/'.join(problem_names)}问题")
        
        # 人群适配说明
        user_groups = set(profile.get('users', []))
        product_groups = set(product.get('user_groups', []))
        matched_groups = user_groups & product_groups
        if matched_groups:
            group_names = [self.USER_GROUPS[g]['name'] for g in matched_groups]
            reasons.append(f"特别适合{'/'.join(group_names)}使用")
        
        # 特色功能说明
        if product.get('features'):
            reasons.append(f"配备{product['features'][0]}等核心技术")
        
        return reasons[:4]  # 最多返回4条原因
    
    def _generate_profile_summary(self, profile: Dict) -> Dict:
        """生成用户需求摘要"""
        return {
            'area': f"{profile.get('area', '未知')}㎡",
            'region': self.REGION_CHARACTERISTICS.get(profile.get('region'), {}).get('name', '未知'),
            'problems': [self.AIR_PROBLEMS.get(p, {}).get('name', p) for p in profile.get('problems', [])],
            'users': [self.USER_GROUPS.get(u, {}).get('name', u) for u in profile.get('users', [])],
            'space_type': self.SPACE_TYPES.get(profile.get('space_type'), {}).get('name', '未知'),
            'budget': self.BUDGET_RANGES.get(profile.get('budget'), {}).get('range', '未知')
        }
    
    # ==================== 选项生成方法 ====================
    
    def _get_area_options(self) -> List[Dict]:
        """获取面积选项"""
        return [
            {'value': '20', 'label': '20㎡以下', 'description': '小卧室/书房'},
            {'value': '30', 'label': '20-40㎡', 'description': '卧室/小客厅'},
            {'value': '50', 'label': '40-60㎡', 'description': '客厅/大卧室'},
            {'value': '80', 'label': '60-100㎡', 'description': '大客厅/开放空间'},
            {'value': '120', 'label': '100㎡以上', 'description': '全屋/大型空间'}
        ]
    
    def _get_region_options(self) -> List[Dict]:
        """获取区域选项"""
        return [
            {'value': 'north', 'label': '北方地区', 'description': '京津冀、东北、西北等'},
            {'value': 'south', 'label': '南方地区', 'description': '长三角、珠三角、西南等'},
            {'value': 'coastal', 'label': '沿海地区', 'description': '沿海城市'},
            {'value': 'inland', 'label': '内陆地区', 'description': '中部内陆城市'},
            {'value': 'industrial', 'label': '工业区附近', 'description': '工业园区周边'}
        ]
    
    def _get_problems_options(self) -> List[Dict]:
        """获取空气问题选项"""
        return [
            {'value': 'pm25', 'label': 'PM2.5/雾霾', 'icon': '🌫️'},
            {'value': 'formaldehyde', 'label': '甲醛/装修污染', 'icon': '🏠'},
            {'value': 'allergen', 'label': '过敏原/花粉', 'icon': '🌸'},
            {'value': 'bacteria', 'label': '细菌/病毒', 'icon': '🦠'},
            {'value': 'odor', 'label': '异味/烟味', 'icon': '💨'},
            {'value': 'dust', 'label': '灰尘/毛发', 'icon': '✨'}
        ]
    
    def _get_users_options(self) -> List[Dict]:
        """获取使用人群选项"""
        return [
            {'value': 'baby', 'label': '婴幼儿', 'icon': '👶'},
            {'value': 'elderly', 'label': '老年人', 'icon': '👴'},
            {'value': 'pregnant', 'label': '孕妇', 'icon': '🤰'},
            {'value': 'allergy', 'label': '过敏人群', 'icon': '🤧'},
            {'value': 'respiratory', 'label': '呼吸道疾病患者', 'icon': '🫁'},
            {'value': 'pet', 'label': '宠物家庭', 'icon': '🐾'},
            {'value': 'general', 'label': '普通成人', 'icon': '👨‍👩‍👧‍👦'}
        ]
    
    def _get_space_options(self) -> List[Dict]:
        """获取空间类型选项"""
        return [
            {'value': 'bedroom', 'label': '卧室', 'description': '需要静音设计'},
            {'value': 'living', 'label': '客厅', 'description': '需要大风量'},
            {'value': 'nursery', 'label': '婴儿房', 'description': '需要超静音+安全'},
            {'value': 'office', 'label': '办公室', 'description': '需要长时间运行'},
            {'value': 'whole_house', 'label': '全屋使用', 'description': '需要大CADR值'}
        ]
    
    def _get_budget_options(self) -> List[Dict]:
        """获取预算选项"""
        return [
            {'value': 'economy', 'label': '经济型', 'range': '1000-2000元'},
            {'value': 'standard', 'label': '标准型', 'range': '2000-4000元'},
            {'value': 'premium', 'label': '高端型', 'range': '4000-8000元'},
            {'value': 'luxury', 'label': '旗舰型', 'range': '8000元以上'}
        ]
    
    # ==================== 输入匹配方法 ====================
    
    def _match_region(self, user_input: str) -> str:
        """匹配用户输入的区域"""
        input_lower = user_input.lower()
        
        region_keywords = {
            'north': ['北方', '北京', '天津', '河北', '东北', '西北', '山西', '内蒙'],
            'south': ['南方', '上海', '广东', '广州', '深圳', '江苏', '浙江', '福建', '湖南', '湖北', '四川', '重庆'],
            'coastal': ['沿海', '海边', '青岛', '大连', '厦门', '海南', '宁波'],
            'inland': ['内陆', '中部', '河南', '安徽', '江西', '山东'],
            'industrial': ['工业', '工厂', '园区']
        }
        
        for region, keywords in region_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    return region
        
        # 默认返回北方
        return 'north'
    
    def _match_space(self, user_input: str) -> str:
        """匹配用户输入的空间类型"""
        input_lower = user_input.lower()
        
        space_keywords = {
            'bedroom': ['卧室', '睡房', '房间'],
            'living': ['客厅', '大厅', '起居'],
            'nursery': ['婴儿房', '儿童房', '宝宝房'],
            'office': ['办公', '书房', '工作'],
            'whole_house': ['全屋', '整屋', '全家', '多房间']
        }
        
        for space, keywords in space_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    return space
        
        return 'living'  # 默认客厅
    
    def _match_budget(self, user_input: str) -> str:
        """匹配用户输入的预算"""
        input_lower = user_input.lower()
        
        if '经济' in input_lower or '1000' in input_lower or '便宜' in input_lower:
            return 'economy'
        elif '标准' in input_lower or '2000' in input_lower or '3000' in input_lower:
            return 'standard'
        elif '高端' in input_lower or '4000' in input_lower or '5000' in input_lower or '6000' in input_lower:
            return 'premium'
        elif '旗舰' in input_lower or '8000' in input_lower or '顶级' in input_lower or '最好' in input_lower:
            return 'luxury'
        
        return 'standard'  # 默认标准型
    
    def _parse_multi_select(self, user_input: str, options_dict: Dict) -> List[str]:
        """解析多选输入"""
        selected = []
        input_lower = user_input.lower()
        
        for key, value in options_dict.items():
            name = value.get('name', '')
            if name in input_lower or key in input_lower:
                selected.append(key)
        
        return selected

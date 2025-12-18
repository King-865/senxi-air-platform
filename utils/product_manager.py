"""
产品管理模块
森系智韵智能空气管理平台
"""
from typing import Dict, List, Optional


class ProductManager:
    """产品数据管理类"""
    
    def __init__(self):
        """初始化产品数据"""
        self.products = self._init_products()
        self.categories = self._init_categories()
    
    def _init_products(self) -> List[Dict]:
        """初始化产品数据库"""
        return [
            {
                'id': 'mini-01',
                'name': '净界者·自然守护Mini',
                'series': '自然守护',
                'category': 'home',
                'price': 1299,
                'original_price': 1599,
                'discount': '19%',
                'cadr_pm25': 200,
                'cadr_formaldehyde': 60,
                'applicable_area': '14-24㎡',
                'noise_range': '25-48dB',
                'power': '6-35W',
                'dimensions': '220×220×380mm',
                'weight': '3.2kg',
                'filter_life': '6-8个月',
                'features': [
                    'HEPA H12高效滤网',
                    '三档风速调节',
                    '静音睡眠模式',
                    '滤芯更换提醒',
                    '触控操作面板'
                ],
                'highlights': [
                    {'icon': 'shield', 'title': 'H12级过滤', 'desc': '99.5%过滤效率'},
                    {'icon': 'volume-x', 'title': '超静音', 'desc': '最低25dB'},
                    {'icon': 'zap', 'title': '节能省电', 'desc': '最低6W功耗'}
                ],
                'suitable_for': ['bedroom', 'nursery', 'office', 'small_room'],
                'problems': ['pm25', 'dust', 'allergen'],
                'user_groups': ['general', 'baby'],
                'images': [
                    '/static/images/products/mini-1.png',
                    '/static/images/products/mini-2.png',
                    '/static/images/products/mini-3.png'
                ],
                'main_image': '/static/images/products/mini.png',
                'rating': 4.7,
                'reviews': 2356,
                'sales': 15680,
                'tags': ['入门首选', '静音设计', '高性价比'],
                'badge': '热销',
                'badge_color': 'orange',
                'stock': 'in_stock',
                'links': {
                    'tmall': 'https://detail.tmall.com/item.htm?id=xxx',
                    'jd': 'https://item.jd.com/xxx.html'
                }
            },
            {
                'id': 'pro-01',
                'name': '净界者·森林呼吸Pro',
                'series': '森林呼吸',
                'category': 'home',
                'price': 2999,
                'original_price': 3599,
                'discount': '17%',
                'cadr_pm25': 450,
                'cadr_formaldehyde': 200,
                'applicable_area': '31-54㎡',
                'noise_range': '28-55dB',
                'power': '8-58W',
                'dimensions': '280×280×520mm',
                'weight': '5.8kg',
                'filter_life': '8-12个月',
                'features': [
                    'HEPA H13医疗级滤网',
                    '活性炭除醛滤网',
                    '甲醛催化分解技术',
                    '激光PM2.5传感器',
                    '智能空气质量显示',
                    'APP远程控制',
                    '语音助手支持',
                    '定时开关机'
                ],
                'highlights': [
                    {'icon': 'shield-check', 'title': 'H13医疗级', 'desc': '99.97%过滤效率'},
                    {'icon': 'wind', 'title': '除醛专家', 'desc': 'CADR 200m³/h'},
                    {'icon': 'smartphone', 'title': '智能互联', 'desc': 'APP+语音控制'}
                ],
                'suitable_for': ['living', 'bedroom', 'office'],
                'problems': ['pm25', 'formaldehyde', 'odor', 'allergen'],
                'user_groups': ['general', 'allergy', 'pet'],
                'images': [
                    '/static/images/products/pro-1.png',
                    '/static/images/products/pro-2.png',
                    '/static/images/products/pro-3.png'
                ],
                'main_image': '/static/images/products/pro.png',
                'rating': 4.8,
                'reviews': 5621,
                'sales': 28950,
                'tags': ['销量冠军', '除醛专家', '智能互联'],
                'badge': '爆款',
                'badge_color': 'red',
                'stock': 'in_stock',
                'links': {
                    'tmall': 'https://detail.tmall.com/item.htm?id=xxx',
                    'jd': 'https://item.jd.com/xxx.html'
                }
            },
            {
                'id': 'max-01',
                'name': '净界者·清新之风Max',
                'series': '清新之风',
                'category': 'home',
                'price': 5999,
                'original_price': 7299,
                'discount': '18%',
                'cadr_pm25': 800,
                'cadr_formaldehyde': 400,
                'applicable_area': '56-96㎡',
                'noise_range': '30-58dB',
                'power': '10-75W',
                'dimensions': '350×350×680mm',
                'weight': '9.5kg',
                'filter_life': '12-18个月',
                'features': [
                    'HEPA H13+双重活性炭',
                    'UV-C紫外线消毒',
                    '负离子净化',
                    '甲醛数显监测',
                    '全屋空气互联',
                    '多房间联动控制',
                    '空气质量报告',
                    '滤芯智能监测'
                ],
                'highlights': [
                    {'icon': 'home', 'title': '全屋净化', 'desc': 'CADR 800m³/h'},
                    {'icon': 'sun', 'title': 'UV消毒', 'desc': '99.9%杀菌率'},
                    {'icon': 'activity', 'title': '甲醛数显', 'desc': '实时精准监测'}
                ],
                'suitable_for': ['living', 'whole_house', 'villa'],
                'problems': ['pm25', 'formaldehyde', 'bacteria', 'odor', 'allergen', 'dust'],
                'user_groups': ['general', 'baby', 'elderly', 'pregnant', 'respiratory'],
                'images': [
                    '/static/images/products/max-1.png',
                    '/static/images/products/max-2.png',
                    '/static/images/products/max-3.png'
                ],
                'main_image': '/static/images/products/max.png',
                'rating': 4.9,
                'reviews': 3892,
                'sales': 12350,
                'tags': ['旗舰之选', '全能净化', '医疗级'],
                'badge': '旗舰',
                'badge_color': 'purple',
                'stock': 'in_stock',
                'links': {
                    'tmall': 'https://detail.tmall.com/item.htm?id=xxx',
                    'jd': 'https://item.jd.com/xxx.html'
                }
            },
            {
                'id': 'uv-01',
                'name': '净界者·紫光卫士',
                'series': '紫光卫士',
                'category': 'home',
                'price': 3999,
                'original_price': 4599,
                'discount': '13%',
                'cadr_pm25': 380,
                'cadr_formaldehyde': 150,
                'applicable_area': '26-46㎡',
                'noise_range': '26-52dB',
                'power': '8-50W',
                'dimensions': '260×260×480mm',
                'weight': '5.2kg',
                'filter_life': '8-12个月',
                'features': [
                    'HEPA H13医疗级滤网',
                    'UV-C深紫外消毒',
                    '等离子杀菌技术',
                    '病毒过滤认证',
                    '儿童安全锁',
                    '零臭氧设计',
                    '医疗机构认证'
                ],
                'highlights': [
                    {'icon': 'zap', 'title': 'UV-C消毒', 'desc': '深紫外杀菌'},
                    {'icon': 'shield', 'title': '医疗认证', 'desc': '专业级防护'},
                    {'icon': 'baby', 'title': '母婴安全', 'desc': '零臭氧设计'}
                ],
                'suitable_for': ['nursery', 'bedroom', 'hospital', 'elderly_room'],
                'problems': ['bacteria', 'pm25', 'allergen', 'virus'],
                'user_groups': ['baby', 'elderly', 'pregnant', 'respiratory'],
                'images': [
                    '/static/images/products/uv-1.png',
                    '/static/images/products/uv-2.png',
                    '/static/images/products/uv-3.png'
                ],
                'main_image': '/static/images/products/uv.png',
                'rating': 4.8,
                'reviews': 1876,
                'sales': 8920,
                'tags': ['杀菌专家', '母婴优选', '医疗级'],
                'badge': '医疗级',
                'badge_color': 'blue',
                'stock': 'in_stock',
                'links': {
                    'tmall': 'https://detail.tmall.com/item.htm?id=xxx',
                    'jd': 'https://item.jd.com/xxx.html'
                }
            },
            {
                'id': 'car-01',
                'name': '净界者·车载清风',
                'series': '车载系列',
                'category': 'car',
                'price': 699,
                'original_price': 899,
                'discount': '22%',
                'cadr_pm25': 30,
                'cadr_formaldehyde': 15,
                'applicable_area': '车内空间',
                'noise_range': '≤35dB',
                'power': '5W',
                'dimensions': '80×80×180mm',
                'weight': '0.5kg',
                'filter_life': '3-6个月',
                'features': [
                    'HEPA H11滤网',
                    '活性炭除味',
                    '负离子清新',
                    'USB供电',
                    '便携设计',
                    '车载支架'
                ],
                'highlights': [
                    {'icon': 'car', 'title': '车载专用', 'desc': '完美适配'},
                    {'icon': 'wind', 'title': '快速净化', 'desc': '10分钟见效'},
                    {'icon': 'plug', 'title': 'USB供电', 'desc': '即插即用'}
                ],
                'suitable_for': ['car'],
                'problems': ['odor', 'pm25', 'formaldehyde'],
                'user_groups': ['general', 'driver'],
                'images': [
                    '/static/images/products/car-1.png',
                    '/static/images/products/car-2.png'
                ],
                'main_image': '/static/images/products/car.png',
                'rating': 4.6,
                'reviews': 4521,
                'sales': 35680,
                'tags': ['车载必备', '新车除味', '便携小巧'],
                'badge': '热销',
                'badge_color': 'orange',
                'stock': 'in_stock',
                'links': {
                    'tmall': 'https://detail.tmall.com/item.htm?id=xxx',
                    'jd': 'https://item.jd.com/xxx.html'
                }
            },
            {
                'id': 'filter-hepa-01',
                'name': '原装HEPA H13滤芯',
                'series': '耗材配件',
                'category': 'accessory',
                'price': 299,
                'original_price': 349,
                'discount': '14%',
                'applicable_models': ['pro-01', 'max-01', 'uv-01'],
                'filter_life': '8-12个月',
                'features': [
                    'H13级HEPA滤网',
                    '99.97%过滤效率',
                    '原装品质保证'
                ],
                'main_image': '/static/images/products/filter-hepa.png',
                'rating': 4.9,
                'reviews': 2156,
                'sales': 18920,
                'tags': ['原装正品', '高效过滤'],
                'stock': 'in_stock'
            },
            {
                'id': 'filter-carbon-01',
                'name': '活性炭除醛滤芯',
                'series': '耗材配件',
                'category': 'accessory',
                'price': 199,
                'original_price': 249,
                'discount': '20%',
                'applicable_models': ['pro-01', 'max-01'],
                'filter_life': '6-8个月',
                'features': [
                    '椰壳活性炭',
                    '高效除醛除味',
                    '大容量吸附'
                ],
                'main_image': '/static/images/products/filter-carbon.png',
                'rating': 4.8,
                'reviews': 1823,
                'sales': 15680,
                'tags': ['除醛专用', '原装正品'],
                'stock': 'in_stock'
            }
        ]
    
    def _init_categories(self) -> List[Dict]:
        """初始化产品分类"""
        return [
            {'id': 'all', 'name': '全部产品', 'icon': 'grid'},
            {'id': 'home', 'name': '家用净化器', 'icon': 'home'},
            {'id': 'car', 'name': '车载净化器', 'icon': 'car'},
            {'id': 'accessory', 'name': '滤芯配件', 'icon': 'package'}
        ]
    
    def get_all_products(self) -> List[Dict]:
        """获取所有产品"""
        return self.products
    
    def get_featured_products(self) -> List[Dict]:
        """获取推荐产品（首页展示）"""
        # 返回家用净化器中的热门产品
        featured_ids = ['mini-01', 'pro-01', 'max-01']
        return [p for p in self.products if p['id'] in featured_ids]
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """根据ID获取产品"""
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def get_products(self, category: str = None, sort_by: str = 'default') -> List[Dict]:
        """获取产品列表（支持筛选和排序）"""
        products = self.products.copy()
        
        # 分类筛选
        if category and category != 'all':
            products = [p for p in products if p.get('category') == category]
        
        # 排序
        if sort_by == 'price_asc':
            products.sort(key=lambda x: x.get('price', 0))
        elif sort_by == 'price_desc':
            products.sort(key=lambda x: x.get('price', 0), reverse=True)
        elif sort_by == 'rating':
            products.sort(key=lambda x: x.get('rating', 0), reverse=True)
        elif sort_by == 'sales':
            products.sort(key=lambda x: x.get('sales', 0), reverse=True)
        
        return products
    
    def get_categories(self) -> List[Dict]:
        """获取产品分类"""
        return self.categories
    
    def get_related_products(self, product_id: str, limit: int = 3) -> List[Dict]:
        """获取相关产品推荐"""
        current = self.get_product_by_id(product_id)
        if not current:
            return []
        
        related = []
        current_category = current.get('category')
        current_problems = set(current.get('problems', []))
        
        for product in self.products:
            if product['id'] == product_id:
                continue
            
            # 计算相关度
            score = 0
            if product.get('category') == current_category:
                score += 2
            
            product_problems = set(product.get('problems', []))
            score += len(current_problems & product_problems)
            
            if score > 0:
                related.append({'product': product, 'score': score})
        
        # 按相关度排序
        related.sort(key=lambda x: x['score'], reverse=True)
        
        return [r['product'] for r in related[:limit]]
    
    def compare_products(self, product_ids: List[str]) -> Dict:
        """产品对比"""
        products = [self.get_product_by_id(pid) for pid in product_ids]
        products = [p for p in products if p is not None]
        
        if len(products) < 2:
            return {'error': '至少需要2个产品进行对比'}
        
        # 对比维度
        comparison = {
            'products': products,
            'dimensions': [
                {
                    'name': '价格',
                    'key': 'price',
                    'unit': '元',
                    'values': [p.get('price', 0) for p in products],
                    'best': 'low'
                },
                {
                    'name': 'PM2.5 CADR',
                    'key': 'cadr_pm25',
                    'unit': 'm³/h',
                    'values': [p.get('cadr_pm25', 0) for p in products],
                    'best': 'high'
                },
                {
                    'name': '甲醛 CADR',
                    'key': 'cadr_formaldehyde',
                    'unit': 'm³/h',
                    'values': [p.get('cadr_formaldehyde', 0) for p in products],
                    'best': 'high'
                },
                {
                    'name': '适用面积',
                    'key': 'applicable_area',
                    'unit': '',
                    'values': [p.get('applicable_area', '-') for p in products],
                    'best': None
                },
                {
                    'name': '噪音范围',
                    'key': 'noise_range',
                    'unit': '',
                    'values': [p.get('noise_range', '-') for p in products],
                    'best': 'low'
                },
                {
                    'name': '用户评分',
                    'key': 'rating',
                    'unit': '分',
                    'values': [p.get('rating', 0) for p in products],
                    'best': 'high'
                }
            ]
        }
        
        return comparison
    
    def search_products(self, keyword: str) -> List[Dict]:
        """搜索产品"""
        keyword = keyword.lower()
        results = []
        
        for product in self.products:
            # 搜索名称、系列、标签
            if (keyword in product.get('name', '').lower() or
                keyword in product.get('series', '').lower() or
                any(keyword in tag.lower() for tag in product.get('tags', []))):
                results.append(product)
        
        return results

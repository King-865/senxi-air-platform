# 森系智韵智能空气管理平台

> 专业空气净化解决方案，守护每一次呼吸

## 项目简介

森系智韵智能空气管理平台是一个以用户空气健康需求为核心构建的综合型数字服务平台。平台突破传统空气净化产品电商仅以商品销售为导向的模式，通过系统化整合智能技术、专业内容、社群互动与品牌服务能力，打造集空气管理方案制定、产品选购、知识传播与持续服务于一体的空气健康生态体系。

## 核心功能

### 1. 智能导购系统
- 多轮对话式交互
- 基于用户需求的智能推荐
- 区域空气特征分析
- 个性化方案生成

### 2. 产品展示中心
- 完整的产品信息展示
- 多维度产品对比
- 用户评价系统
- 详细规格参数

### 3. AI空气管家
- 24小时在线咨询
- 智能问答服务
- 产品推荐
- 售后支持

### 4. 空气研究院
- 空气质量科普知识
- AQI指数解读
- 污染物危害分析
- HEPA技术原理

### 5. 健康呼吸社区
- 用户经验分享
- 话题讨论
- 会员成长体系
- 内容创作激励

### 6. 品牌展示
- 品牌发展历程
- 核心技术介绍
- 权威认证展示
- 合作伙伴链接

## 技术栈

- **后端框架**: Python Flask
- **前端框架**: HTML5 + TailwindCSS
- **图标库**: Lucide Icons
- **字体**: Noto Sans SC

## 项目结构

```
senxi-air-platform/
├── app.py                 # Flask主应用
├── requirements.txt       # Python依赖
├── README.md             # 项目说明
├── static/               # 静态资源
│   ├── css/
│   │   └── style.css     # 自定义样式
│   ├── js/
│   │   └── main.js       # 主JavaScript文件
│   └── images/           # 图片资源
├── templates/            # 页面模板
│   ├── base.html         # 基础模板
│   └── pages/
│       ├── index.html          # 首页
│       ├── products.html       # 产品中心
│       ├── product_detail.html # 产品详情
│       ├── smart_guide.html    # 智能导购
│       ├── research.html       # 空气研究院
│       ├── community.html      # 健康社区
│       └── brand.html          # 品牌故事
└── utils/                # 工具模块
    ├── __init__.py
    ├── smart_guide.py    # 智能导购系统
    ├── air_butler.py     # AI空气管家
    └── product_manager.py # 产品管理
```

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/senxi-air-platform.git
cd senxi-air-platform
```

2. 创建虚拟环境（可选）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python app.py
```

5. 访问应用
打开浏览器访问 `http://localhost:5000`

## 功能演示

### 智能导购流程

1. 进入智能导购页面
2. 回答关于房屋面积的问题
3. 选择居住区域
4. 选择关注的空气问题（可多选）
5. 选择家庭成员类型
6. 选择使用空间
7. 选择预算范围
8. 获取个性化产品推荐

### AI空气管家

- 点击页面右下角的聊天按钮
- 选择快捷回复或输入问题
- 获取智能回答和建议

## API接口

### 智能导购

```
POST /api/guide/start
POST /api/guide/chat
```

### AI空气管家

```
POST /api/butler/chat
```

### 产品相关

```
GET /api/products
GET /api/products/<id>
POST /api/products/recommend
```

## 配置说明

可以通过环境变量或 `.env` 文件配置以下参数：

```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 客服热线：400-888-8888
- 邮箱：service@senxi-air.com
- 官网：https://www.senxi-air.com

---

© 2024 森系智韵. All rights reserved.

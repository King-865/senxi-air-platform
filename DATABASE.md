# 数据库使用说明

## 概述

森系智韵平台使用 **SQLite** 数据库存储用户、产品、订单和社区帖子数据。数据库文件位于 `instance/senxi_air.db`。

## 数据库模型

### 1. User（用户表）

存储用户账号信息、等级积分和OAuth登录信息。

**主要字段：**
- `id`: 用户ID（主键）
- `phone`: 手机号（唯一）
- `email`: 邮箱
- `username`: 用户名
- `password_hash`: 密码哈希
- `avatar`: 头像URL
- `level`: 用户等级（L1-L4）
- `points`: 积分
- `wechat_openid`: 微信OpenID
- `qq_openid`: QQ OpenID
- `github_id`: GitHub ID

### 2. Product（产品表）

存储产品信息和库存数据。

**主要字段：**
- `id`: 产品ID（主键）
- `product_id`: 产品编号（唯一）
- `name`: 产品名称
- `category`: 产品分类
- `price`: 价格
- `original_price`: 原价
- `stock`: 库存数量 ⭐
- `sales`: 销量
- `description`: 产品描述
- `main_image`: 主图URL
- `images`: 图片列表（JSON）
- `specs`: 规格参数（JSON）
- `features`: 产品特点（JSON）
- `tags`: 标签（JSON）
- `badge`: 徽章文字
- `badge_color`: 徽章颜色
- `rating`: 评分
- `review_count`: 评价数

**库存管理方法：**
- `update_stock(quantity)`: 更新库存（增加/减少）
- `decrease_stock(quantity)`: 销售减库存

### 3. Order（订单表）

存储订单信息和状态。

**主要字段：**
- `id`: 订单ID（主键）
- `order_id`: 订单编号（唯一）
- `user_id`: 用户ID（外键）
- `status`: 订单状态
  - `pending`: 待付款
  - `paid`: 已付款/待发货
  - `shipped`: 已发货/待收货
  - `completed`: 已完成
  - `cancelled`: 已取消
- `total_amount`: 总金额
- `discount_amount`: 优惠金额
- `final_amount`: 实付金额
- `receiver_name`: 收货人姓名
- `receiver_phone`: 收货人电话
- `receiver_address`: 收货地址
- `created_at`: 创建时间
- `paid_at`: 付款时间
- `shipped_at`: 发货时间
- `completed_at`: 完成时间

### 4. OrderItem（订单项表）

存储订单中的商品明细。

**主要字段：**
- `id`: 订单项ID（主键）
- `order_id`: 订单ID（外键）
- `product_id`: 产品ID（外键）
- `product_name`: 产品名称（快照）
- `product_image`: 产品图片（快照）
- `price`: 单价
- `quantity`: 数量
- `subtotal`: 小计

### 5. Post（帖子表）

存储社区帖子内容。

**主要字段：**
- `id`: 帖子ID（主键）
- `post_id`: 帖子编号（唯一）
- `user_id`: 用户ID（外键）
- `title`: 标题
- `content`: 内容
- `category`: 分类
  - `experience`: 使用心得
  - `formaldehyde`: 除甲醛
  - `allergy`: 过敏防护
  - `general`: 综合讨论
- `images`: 图片列表（JSON）
- `likes`: 点赞数
- `views`: 浏览数
- `comment_count`: 评论数
- `is_published`: 是否发布
- `is_pinned`: 是否置顶

### 6. Comment（评论表）

存储帖子评论。

**主要字段：**
- `id`: 评论ID（主键）
- `post_id`: 帖子ID（外键）
- `user_id`: 用户ID（外键）
- `content`: 评论内容
- `parent_id`: 父评论ID（用于回复）
- `likes`: 点赞数

### 7. PostLike（点赞记录表）

存储用户对帖子的点赞记录。

**主要字段：**
- `id`: 记录ID（主键）
- `post_id`: 帖子ID（外键）
- `user_id`: 用户ID（外键）

**唯一约束：** 一个用户只能给一个帖子点赞一次

## 数据库初始化

### 首次初始化

```bash
# 进入项目目录
cd senxi-air-platform

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（创建表并填充示例数据）
python init_db.py
```

### 重置数据库

如果需要清空数据并重新初始化：

```bash
# 删除数据库文件
rm -rf instance/

# 重新初始化
python init_db.py
```

## 测试数据库

运行测试脚本验证数据库功能：

```bash
python test_db.py
```

测试内容包括：
- 用户表查询
- 产品表查询和库存管理
- 帖子表查询
- 用户密码验证
- 关联查询（用户-帖子）

## 示例数据

初始化后会创建以下示例数据：

### 用户（4个）
- 清新小屋（13800138001）
- 过敏星人（13800138002）
- 科技宅（13800138003）
- 宝妈日记（13800138004）

**默认密码：** 123456

### 产品（5个）
1. 净界者·森林呼吸Pro（¥2999，库存50）
2. 净界者·清新之风Max（¥4999，库存30）
3. 净界者·守护天使（¥1899，库存80）
4. 净界者·车载清风（¥599，库存120）
5. H13级HEPA复合滤芯（¥299，库存200）

### 帖子（4个）
1. 新房除甲醛三个月心得分享
2. 过敏体质的救星！用了半年的真实感受
3. 清新之风Max开箱评测
4. 给宝宝房间选的守护天使，太安静了

## 在代码中使用数据库

### 查询示例

```python
from models import db, User, Product, Post

# 查询所有产品
products = Product.query.all()

# 根据ID查询产品
product = Product.query.filter_by(product_id='prod_001').first()

# 查询库存充足的产品
in_stock_products = Product.query.filter(Product.stock > 0).all()

# 查询用户的所有帖子
user = User.query.filter_by(phone='13800138001').first()
user_posts = user.posts.all()
```

### 添加数据

```python
from models import db, Product

# 创建新产品
new_product = Product(
    product_id='prod_006',
    name='新产品',
    category='home',
    price=1999,
    stock=100
)

# 添加到数据库
db.session.add(new_product)
db.session.commit()
```

### 更新数据

```python
# 更新库存
product = Product.query.filter_by(product_id='prod_001').first()
product.decrease_stock(5)  # 销售5件
db.session.commit()
```

### 删除数据

```python
# 删除产品
product = Product.query.filter_by(product_id='prod_006').first()
db.session.delete(product)
db.session.commit()
```

## 数据库文件位置

- **开发环境：** `instance/senxi_air.db`
- **生产环境：** 建议使用 PostgreSQL 或 MySQL

## 注意事项

1. **数据库文件不提交到Git**：`instance/` 目录已添加到 `.gitignore`
2. **密码安全**：用户密码使用 `werkzeug.security` 进行哈希存储
3. **库存管理**：使用 `decrease_stock()` 方法确保库存不会为负数
4. **事务处理**：重要操作记得 `db.session.commit()`
5. **生产环境**：SQLite 适合开发和小型应用，大型应用建议使用 PostgreSQL

## 数据库迁移

如果需要修改数据库结构，建议使用 Flask-Migrate：

```bash
pip install flask-migrate

# 初始化迁移
flask db init

# 生成迁移脚本
flask db migrate -m "描述"

# 应用迁移
flask db upgrade
```

## 备份与恢复

### 备份数据库

```bash
cp instance/senxi_air.db instance/senxi_air_backup_$(date +%Y%m%d).db
```

### 恢复数据库

```bash
cp instance/senxi_air_backup_20241223.db instance/senxi_air.db
```

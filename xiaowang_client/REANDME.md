# 客户信息登记与查询系统

## 项目简介
基于 Django 开发的客户信息管理系统，支持销售人员登记、搜索、筛选、编辑和删除客户信息。每个销售只能管理自己的客户，管理员可在后台查看所有数据。

## 功能列表
- ✅ 用户注册/登录/登出
- ✅ 客户信息创建（姓名、手机号、来源渠道、备注）
- ✅ 客户列表展示（按时间倒序，最多5条）
- ✅ 手机号模糊搜索 + 来源渠道筛选（AJAX 无刷新）
- ✅ 客户信息编辑与更新
- ✅ 删除客户（确认弹窗 + 无刷新移除）
- ✅ 权限控制：用户仅见自己数据，管理员可看全部

## 技术栈
- 后端：Django 4.2
- 前端：Bootstrap 5 + 原生 JavaScript
- 数据库：SQLite

## 快速开始

### 1. 克隆项目
git clone https://github.com/wuming-is-god/my-web-repository.git
cd my-web-repository.git

### 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. 安装依赖
pip install -r requirements.txt

### 4. 数据库迁移
python manage.py migrate

### 5. 创建管理员
python manage.py createsuperuser

### 6. 运行
python manage.py runserver

### 7. 访问
- 客户系统：http://127.0.0.1:8000/login/
- 管理后台：http://127.0.0.1:8000/admin/

## 项目结构
├── client/ # 应用目录
│ ├── models.py # 数据模型
│ ├── views.py # 视图
│ ├── forms.py # 表单
│ ├── urls.py # 路由
│ └── templates/ # 模板
├── config/ # 项目配置
└── static/ # 静态文件

## 在线演示
[部署链接]（部署后补充）

## 作者
[你的名字] - 2026年
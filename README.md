# SimpleFlaskProject - One Piece Flask App

这是一个基于 Flask 的 Web 应用程序，采用了 MVC 架构，并以《海贼王》（One Piece）为主题。项目集成了 SQLAlchemy ORM、MySQL 数据库、JWT 认证等功能，并支持 Docker 容器化部署。

## 🛠 技术栈

- **Web 框架**: Flask 3.0
- **数据库**: MySQL, Flask-SQLAlchemy, PyMySQL
- **认证**: PyJWT
- **部署**: Docker, Docker Compose
- **其他**: Flask-CORS, Makefile

## 🚀 快速开始 (推荐使用 Docker)

本项目提供了 `Makefile` 和 Docker 配置，可以一键启动所有服务。

### 前置要求
- Docker
- Docker Compose

### 常用命令

```bash
# 启动所有服务 (Web 应用 + MySQL)
make up

# 查看日志
make logs

# 停止服务
make down

# 构建镜像
make build

# 清理环境
make clean
```

启动成功后，访问：[http://localhost:8080](http://localhost:8080)

## 💻 本地开发

如果你想在本地直接运行 Python 代码：

1.  **创建虚拟环境**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置数据库**
    - 确保你有一个运行中的 MySQL 数据库。
    - 修改 `onepiece/config.py` 或设置环境变量以匹配你的数据库配置。
    - 可以使用 `init.sql` 初始化数据库结构。

4.  **运行应用**
    ```bash
    python onepiece/app.py
    ```

## 👤 测试账号

系统预置了以下测试账号：

- **管理员**: `admin` / `admin123`
- **普通用户**: `user` / `user123`

## 📂 项目结构

```
SimpleFlaskProject/
├── onepiece/               # 应用源码
│   ├── controllers/        # 控制器 (蓝图)
│   ├── models/             # 数据模型 (SQLAlchemy)
│   ├── static/             # 静态资源 (图片, HTML)
│   ├── utils/              # 工具函数
│   ├── app.py              # 应用工厂与入口
│   └── config.py           # 配置文件
├── docker-compose.yml      # Docker 编排
├── Dockerfile              # Docker 构建文件
├── Makefile                # 常用命令管理
├── requirements.txt        # Python 依赖
├── init.sql                # 数据库初始化脚本
└── API.md                  # API 接口文档
```

## 📝 文档

更多关于 API 的详细信息，请参考 [API.md](API.md)。
类的分析与设计请参考 [CLASS_ANALYSIS.md](CLASS_ANALYSIS.md)。

# Jenkins CI/CD 配置指南

本指南将帮助你使用 Jenkins 设置本项目的自动化构建和部署流程。

## 1. 预置条件

你的 Jenkins 服务器需要安装以下插件：
- **Docker Pipeline**: 用于支持 Docker 容器内的构建和 Docker 命令。
- **Pipeline**: 核心流水线插件。
- **SSH Agent** 或 **SSH Credentials**: 用于远程部署。
- **Git**: 用于拉取代码。

并且 Jenkins Agent (构建节点) 需要安装：
- **Docker**: 能够执行 `docker` 命令。
- **Git**: 能够拉取代码。

## 2. 凭据配置 (Credentials)

在 Jenkins 首页 -> **Manage Jenkins** -> **Manage Credentials** 中添加以下凭据：

### 1. Docker Hub 凭据
- **类型**: Username with password
- **ID**: `docker-hub-creds`
- **Username**: 你的 Docker Hub 用户名
- **Password**: 你的 Docker Hub 密码或 Access Token

### 2. 部署服务器 SSH 密钥
- **类型**: SSH Username with private key
- **ID**: `deploy-ssh-key`
- **Username**: 生产服务器的登录用户名 (例如 `root` 或 `ubuntu`)
- **Private Key**: 能够登录生产服务器的 SSH 私钥

### 3. 数据库凭据
- **类型**: Username with password
- **ID**: `db-creds`
- **Username**: 生产环境数据库用户名
- **Password**: 生产环境数据库密码

## 3. 环境变量配置

建议在 Jenkins 的 **Manage Jenkins** -> **Configure System** -> **Global properties** -> **Environment variables** 中配置以下变量，或者在具体 Job 中配置：

- `PROD_HOST`: 生产服务器的 IP 地址 (例如 `192.168.1.100`)
- `DB_HOST`: 生产数据库的主机地址 (例如 `mysql-prod`)
- `DB_NAME`: 生产数据库名称 (例如 `onepiece_prod`)

## 4. 创建流水线任务 (Pipeline Job)

1.  点击 **New Item**。
2.  输入任务名称 (例如 `simple-flask-cicd`)，选择 **Pipeline**，点击 OK。
3.  在 **Pipeline** 部分：
    - **Definition**: 选择 `Pipeline script from SCM`。
    - **SCM**: 选择 `Git`。
    - **Repository URL**: 输入本项目的 Git 仓库地址。
    - **Branch Specifier**: `*/main` (或者留空监听所有分支)。
    - **Script Path**: 确保为 `Jenkinsfile`。
4.  点击 **Save**。

## 5. 运行流水线

- 点击 **Build Now** 手动触发构建。
- 也可以配置 **Build Triggers** (例如 `GitHub hook trigger for GITScm polling`) 来实现代码提交自动触发。

## 6. 流水线流程说明

1.  **Test & Lint**:
    - 启动 `python:3.11` Docker 容器。
    - 安装依赖并运行 `flake8` 和 `pytest`。
2.  **Build & Push Docker** (仅 main 分支):
    - 登录 Docker Hub。
    - 构建 Docker 镜像并打上标签 (`latest` 和 `BUILD_NUMBER`)。
    - 推送镜像到 Docker Hub。
3.  **Deploy to Production** (仅 main 分支):
    - 通过 SSH 连接到 `PROD_HOST`。
    - 拉取最新镜像。
    - 停止并删除旧容器。
    - 启动新容器并注入环境变量。

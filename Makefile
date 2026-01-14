.PHONY: help build up down logs restart clean install lint test docker-build docker-push frontend-install frontend-dev

# 默认变量
IMAGE ?= simple-flask-project
TAG ?= latest

help:  ## 显示帮助信息
	@echo "可用命令："
	@echo "  make build         - 构建Docker镜像 (docker-compose)"
	@echo "  make up            - 启动所有后端服务"
	@echo "  make down          - 停止所有服务"
	@echo "  make logs          - 查看日志"
	@echo "  make restart       - 重启服务"
	@echo "  make clean         - 清理所有容器和数据卷"
	@echo "  --- 前端开发 ---"
	@echo "  make frontend-install - 安装前端依赖"
	@echo "  make frontend-dev     - 启动前端开发服务器 (带代理)"
	@echo "  --- CI/CD 命令 ---"
	@echo "  make install       - 安装 Python 依赖"
	@echo "  make lint          - 运行代码检查"
	@echo "  make test          - 运行单元测试"
	@echo "  make docker-build  - 构建指定镜像 (IMAGE=... TAG=...)"
	@echo "  make docker-push   - 推送指定镜像 (IMAGE=... TAG=...)"

build:  ## 构建Docker镜像 (本地开发用)
	docker-compose build

up:  ## 启动所有服务
	docker-compose up -d
	@echo "✅ 后端服务已启动！访问 http://localhost:8080 (仅API)"
	@echo "💡 提示: 运行 'make frontend-dev' 启动前端开发页面"

down:  ## 停止所有服务
	docker-compose down

logs:  ## 查看日志
	docker-compose logs -f

restart:  ## 重启服务
	docker-compose restart

clean:  ## 清理所有容器和数据卷
	docker-compose down -v
	docker system prune -f

# --- 前端开发 ---

frontend-install: ## 安装前端依赖
	cd frontend && npm install

frontend-dev: ## 启动前端开发服务器 (带代理)
	cd frontend && npm run dev

# --- CI/CD 专用命令 ---

install: ## 安装 Python 依赖
	pip install --upgrade pip
	pip install -r requirements.txt

lint: ## 运行代码检查
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test: ## 运行单元测试
	pytest

docker-build: ## 构建 Docker 镜像 (支持 IMAGE 和 TAG 变量)
	docker build -t $(IMAGE):$(TAG) .

docker-push: ## 推送 Docker 镜像
	docker push $(IMAGE):$(TAG)

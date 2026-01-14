.PHONY: help build up down logs restart clean

help:  ## 显示帮助信息
	@echo "可用命令："
	@echo "  make build    - 构建Docker镜像"
	@echo "  make up       - 启动所有服务"
	@echo "  make down     - 停止所有服务"
	@echo "  make logs     - 查看日志"
	@echo "  make restart  - 重启服务"
	@echo "  make clean    - 清理所有容器和数据卷"

build:  ## 构建Docker镜像
	docker-compose build

up:  ## 启动所有服务
	docker-compose up -d
	@echo "✅ 服务已启动！访问 http://localhost:8080"

down:  ## 停止所有服务
	docker-compose down

logs:  ## 查看日志
	docker-compose logs -f

restart:  ## 重启服务
	docker-compose restart

clean:  ## 清理所有容器和数据卷
	docker-compose down -v
	docker system prune -f
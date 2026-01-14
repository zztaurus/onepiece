-- 初始化SQL脚本（可选，SQLAlchemy会自动创建表）
-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 确保数据库使用UTF8MB4
ALTER DATABASE onepiece_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


# ==================== .env.example ====================
# MySQL配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=onepiece_user
MYSQL_PASSWORD=onepiece_pass_2024
MYSQL_DATABASE=onepiece_db

# Flask配置
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
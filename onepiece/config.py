"""
应用配置文件
"""
import os


class Config:
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'onepiece_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'onepiece_pass_2024')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'onepiece_db')

    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 开发环境打印SQL语句

    # JWT配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

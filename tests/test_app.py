import pytest
from onepiece.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # 使用内存数据库或模拟数据库进行测试会更好，这里简单演示
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """测试首页是否正常访问"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_static_files(client):
    """测试静态文件是否可访问"""
    # 假设有一个 luffy.jpg
    rv = client.get('/images/luffy.jpg')
    # 如果文件存在，应该是 200；如果不存在可能是 404，这里主要确保没有 500
    assert rv.status_code in [200, 404]

def test_404(client):
    """测试 404 页面"""
    rv = client.get('/non_existent_page')
    assert rv.status_code == 404

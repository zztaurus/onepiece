"""
使用 Jikan API 下载海贼王角色头像
"""
import os
import urllib.request
import ssl
import json
import time

ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_DIR = 'onepiece/static/images'

# MyAnimeList 角色 ID
CHARACTERS = {
    'luffy': 40,
    'zoro': 62,
    'nami': 723,
    'usopp': 724,
    'sanji': 725,
    'chopper': 726,
    'robin': 61,
    'franky': 13378,
    'brook': 13377,
    'jinbe': 16158,
}

def get_image_url(char_id):
    """通过 Jikan API 获取角色图片 URL"""
    api_url = f'https://api.jikan.moe/v4/characters/{char_id}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        return data['data']['images']['jpg']['image_url']

def download_image(url, filepath):
    """下载图片"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        with open(filepath, 'wb') as f:
            f.write(response.read())
    return os.path.getsize(filepath)

def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)

    for name, char_id in CHARACTERS.items():
        filepath = os.path.join(IMAGE_DIR, f'{name}.jpg')

        # 跳过已下载的大文件
        if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
            print(f'✓ {name}.jpg 已存在')
            continue

        print(f'获取 {name} 图片URL...', end=' ')
        try:
            # Jikan API 限流，需要间隔请求
            time.sleep(0.5)
            url = get_image_url(char_id)
            print(f'下载中...', end=' ')
            size = download_image(url, filepath)
            print(f'✓ 完成 ({size} bytes)')
        except Exception as e:
            print(f'✗ 失败: {e}')

if __name__ == '__main__':
    print('使用 Jikan API 下载海贼王角色头像\n')
    main()
    print('\n完成！')

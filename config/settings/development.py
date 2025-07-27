# base.py(共通設定)をdevelopment.py(開発環境設定)にインポートして反映
from .base import *
 
# DBの接続先設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # MySQLと同じ設定
        'NAME': 'app',
        'USER': 'root',
        'PASSWORD': 'Password001',
        'HOST': 'host.docker.internal',
        'PORT': '53306',
        # トランザクション管理
        'ATOMIC_REQUESTS': True
    }
}
**使用时安装：**
`pip install django-iacs-1.0.0.tar`

**修改settings配置：**

INSTALL_APPS = [
	...,
	iacs
	...,
]

ROOT_URLCONF = '项目名.urls'
AUTH_USER_MODEL = 'iacs.User'

---------------------------
在django settings中加入
IACS_SETTINGS = {
	'LOGIN_USER_KEY': 'iacs__user_{user_id}',
	'LOGIN_TOKEN_KEY': 'iacs__user_token_{token}',
	'LOGIN_CHANNEL_GROUP_NAME': 'iacs__login_{username}',
	'USER_CHANNEL_NAME': 'iacs__user_channel_{user_id}',
	'GROUP_CHANNEL_NAME': 'iacs__group_channel',
	'REDIS_IP': '127.0.0.1',
	'REDIS_PORT': 6379,
	'REDIS_PASSWORD': '',
	'RUNNING_LOG_NAME': '',
	'ERROR_LOG_NAME': '',
	'ROOT_WEBSOCKET_MESSAGE_ROUTE': '',
    'MENUS': []
}

drf相关修改
REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
    ......,
    'iacs.rest.auth.RedisTokenAuthentication',),  # 使用iacs基于redis的认证模块

    'DEFAULT_PERMISSION_CLASSES': (
    ......,
    'iacs.permission.APIPermission',),  # 添加iacs的API接口权限模块

    ......,
    'DEFAULT_PAGINATION_CLASS': 'iacs.rest.pagination.PageNumberPaginationExtension',
    'EXCEPTION_HANDLER': 'iacs.rest.viewsets.exception_handler',
}

用户登录或修改信息产生的日志通过signal发送出来，由外部的日志模块完成。
在iacs.utils.log中的文件send_log.py定义了信号量user_log,使用signal将信息弹出来交给其他模块处理
在其他模块中导入user_log进行信号的注册和函数的申明，用来实现记录iacs模块产生的日志的功能
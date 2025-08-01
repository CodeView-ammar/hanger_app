import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح السر - يجب حفظه بشكل آمن في الإنتاج
SECRET_KEY = 'django-insecure-o*!@ed@kc*^sc^09=qx+u&r&0kxs(j5cj$!8g5-xo4o#t1i4_l'

# وضع التطوير
DEBUG = True

# النطاقات المسموح بها
ALLOWED_HOSTS = [
    "hanger.metasoft-ar.com",
    "hangerapp.com.sa",
    "*"
]

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # تطبيقات الطرف الثالث
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'channels',

    # التطبيقات الخاصة بك
    'users',
    'invoices',
    'laundries',
    'orders',
    'reviews',
    'services',
    'settings',
    'notification',
    'agent',
    'accounts',
    'support',
    'import_export',
]

ASGI_APPLICATION='hanger_app.asgi.application'
# إعدادات قنوات

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# الوسيطات
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'hanger_app.urls'
WSGI_APPLICATION = 'hanger_app.wsgi.application'

# قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والمنطقة الزمنية
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [
    BASE_DIR / "locale",  # إن أردت تخصيص ترجمات لاحقاً
]
# اللغات المدعومة
LANGUAGES = [
    ('ar', _('العربية')),
    # ('en', _('الإنجليزية')),
]

# مسار ملفات الترجمة
# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]

# الملفات الثابتة والإعلامية
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = '/root/metasoft/metasoft-ar.com/hanger_app/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/root/metasoft/metasoft-ar.com/hanger_app/media'

# نوع المفتاح الأساسي الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# إعدادات المستخدم
AUTH_USER_MODEL = 'users.Users'
# إعدادات Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT Authentication (اختياري)
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# الحجم الأقصى لتحميل البيانات
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

import logging

# إعدادات السجلات (Logging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # تغيير إلى DEBUG لتسجيل جميع الرسائل
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'hanger_app.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',  # يمكنك تركه كـ ERROR أو تغييره إلى DEBUG إذا كنت تريد
            'propagate': True,
        },
        'hanger_app': {
            'handlers': ['file'],
            'level': 'DEBUG',  # تغيير إلى DEBUG لتسجيل جميع الرسائل
            'propagate': False,
        },
    },
}

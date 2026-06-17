# coding: utf-8
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'meshwar-super-secret-key-for-testing-only-123')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.MeshwarConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === الحل الهندسي النهائي لإجبار الجداول على الظهور فوراً ===
try:
    import django
    django.setup()
    from django.core.management import call_command
    from django.db import connection
    
    # 1. المزامنة الإجبارية لتخطي ملفات الهجرة المعطوبة
    call_command('migrate', '--run-syncdb', interactive=False)
    
    # 2. فحص صريح للتأكد من وجود الجدول الفعلي لحل المعضلة
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='apps_shipment';")
        if not cursor.fetchone():
            print("=== تنبيه: جدول apps_shipment مفقود، جاري تخليقه يدوياً ===")
            # أمر طوارئ داخلي لبناء جداول تطبيق apps قسرياً
            call_command('makemigrations', 'apps', interactive=False)
            call_command('migrate', 'apps', interactive=False)
            
    print("=== تم تفعيل ومزامنة قاعدة البيانات بنجاح قطعي ===")
except Exception as e:
    print(f"=== خطأ نظام المزامنة الذاتي: {e} ===")

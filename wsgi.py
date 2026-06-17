# coding: utf-8
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# تشغيل الهجرة تلقائياً وبناء الجداول فور نهوض السيرفر
try:
    from django.core.management import execute_from_command_line
    # تنفيذ أمر migrate بشكل صامت لإنشاء جداول قاعدة البيانات المفقودة
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    print("=== Database tables synced successfully! ===")
except Exception as e:
    print(f"=== Database sync skipped or failed: {e} ===")

application = get_wsgi_application()

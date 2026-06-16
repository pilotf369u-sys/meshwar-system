# coding: utf-8
from django.contrib import admin
from django.urls import path
from views import customer_dashboard, upload_deposit_receipt

urlpatterns = [
    path('admin/', admin.site.urls),  # لوحة تحكم الإدارة والموظفين لتحديث الحالات والباركود
    path('dashboard/', customer_dashboard, name='customer_dashboard'),  # لوحة تتبع الزبون
    path('upload-receipt/', upload_deposit_receipt, name='upload_deposit_receipt'),  # رفع الحوالة
]

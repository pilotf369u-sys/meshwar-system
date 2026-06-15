# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# 1. ملف الموظفين وأرقام الواتساب المرنة
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="الموظف")
    phone_number = models.CharField(max_digits=20, verbose_name="رقم الواتساب الفعال")
    role = models.CharField(max_digits=50, choices=[('Admin', 'مدير عام'), ('Staff', 'موظف فرع')], verbose_name="الصلاحية")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 2. ملف المندوبين وتوجيه الشحنات حسب المحافظة
class Courier(models.Model):
    name = models.CharField(max_digits=100, verbose_name="اسم المندوب المحلي")
    phone = models.CharField(max_digits=20, verbose_name="رقم هاتفه")
    assigned_province = models.CharField(max_digits=100, verbose_name="المحافظة المسؤول عنها")

    def __str__(self):
        return f"المندوب: {self.name} ({self.assigned_province})"

# 3. ملف الزبون والمحفظة الرقمية واختيار الدول الديناميكي
class CustomerProfile(models.Model):
    COUNTRY_CHOICES = [('Turkey', 'تركيا'), ('Iraq', 'العراق')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب الزبون")
    current_country = models.CharField(max_digits=50, choices=COUNTRY_CHOICES, verbose_name="بلد الإقامة الحالي")
    city_province = models.CharField(max_digits=100, verbose_name="المحافظة / الولاية")
    address_details = models.TextField(verbose_name="العنوان التفصيلي")

    def __str__(self):
        return self.user.username

class CustomerWallet(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, verbose_name="الزبون")
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="الرصيد المتاح ($)")
    reward_points = models.IntegerField(default=0, verbose_name="نقاط المكافآت")

    def __str__(self):
        return f"محفظة {self.customer.user.username} - الرصيد: {self.available_balance}$"

# 4. نظام الحوالات اليدوية (الفيزا أو حساب الموظف) برفع الإيصال
class WalletDepositRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'بانتظار مراجعة الموظف وتأكيد التحويل ⏳'),
        ('Approved', 'تم التأكيد وشحن الرصيد بنجاح ✅'),
        ('Rejected', 'تم رفض الحوالة (الإيصال غير واضح) ❌'),
    ]
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="الزبون")
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المحول ($)")
    receipt_image = models.ImageField(upload_to='receipts/', verbose_name="صورة وصل الحوالة")
    payment_method_used = models.CharField(max_digits=150, verbose_name="الحساب أو الموظف المحول إليه")
    status = models.CharField(max_digits=50, choices=STATUS_CHOICES, default='Pending', verbose_name="حالة الطلب")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات الإدارة")
    created_at = models.DateTimeField(auto_now_add=True)

# 5. سجل الحركات المالي التاريخي للمحفظة
class WalletTransaction(models.Model):
    wallet = models.ForeignKey(CustomerWallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_digits=50, choices=[('Deposit', 'إيداع'), ('Shipping_Payment', 'أجور شحن')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_digits=255)
    timestamp = models.DateTimeField(auto_now_add=True)

# 6. نظام الشحنات المركزي (مراحل الحالات الـ 9، التحكم بالسعر، الباركود، الفيديوهات)
class Shipment(models.Model):
    STATUS_STAGES = [
        ('1_received_ankara', '1. استلام الطرد في مستودع أنقرة 🏢'),
        ('2_sorting', '2. الفرز والتحضير للشحن الموحد 📦'),
        ('3_loading', '3. جاري تحميل الشحنة الموحدة 🚚'),
        ('4_on_the_way', '4. الشحنة في الطريق الدولي 🗺️'),
        ('5_customs', '5. في التخليص الجمركي 📑'),
        ('6_received_dest_warehouse', '6. وصلت مستودع البلد الوجهة 🏪'),
        ('7_with_courier', '7. الشحنة مع المندوب المحلي 🚴'),
        ('8_delivered', '8. تم التسليم للزبون بنجاح 🎉'),
        ('9_returned', '9. طرد راجع / مرتجع ↩️'),
    ]

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, verbose_name="صاحب الشحنة")
    tracking_number = models.CharField(max_digits=100, unique=True, verbose_name="رقم التتبع الموحد (الباركود)")
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="الوزن الحقيقي (كغم)")
    
    # التحكم المالي المرن بالأسعار
    base_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="التكلفة الأساسية ($)")
    adjustment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="تعديل السعر بالزيادة أو النقصان ($)")
    
    current_status = models.CharField(max_digits=50, choices=STATUS_STAGES, default='1_received_ankara', verbose_name="حالة الشحنة الحالية")
    assigned_courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المندوب المحلي الموجه إليه")
    
    # مساحة الفيديو والإعلانات
    instructional_video_url = models.URLField(blank=True, null=True, verbose_name="رابط فيديو اليوتيوب التعليمي للشحنة")
    show_ads = models.BooleanField(default=True, verbose_name="تفعيل إعلانات جوجل غير المزعجة لهذه الصفحة")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث للحالة")

    @property
    def final_cost(self):
        return self.base_shipping_cost + self.adjustment_amount

    def __str__(self):
        return f"شحنة رقم {self.tracking_number} - {self.get_current_status_display()}"

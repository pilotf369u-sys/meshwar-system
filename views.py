# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from models import Shipment, CustomerProfile, WalletDepositRequest

# 1. واجهة لوحة تحكم الزبون (التتبع، الفيديوهات، والتقييم)
# قمنا بإزالة @login_required مؤقتاً لكي يفتح الموقع معك مباشرة على Render
def customer_dashboard(request):
    # إذا كان المستخدم مسجلاً دخوله، نأتي ببياناته الحقيقية
    if request.user.is_authenticated:
        customer = CustomerProfile.objects.filter(user=request.user).first()
        shipments = Shipment.objects.filter(customer=customer).order_by('-updated_at') if customer else []
    else:
        # إذا كان زائراً عاماً (بدون تسجيل دخول)، نعرض له صفحة فارغة أو بيانات تجريبية بدلاً من قفل الموقع
        customer = None
        shipments = Shipment.objects.all().order_by('-updated_at') # عرض الشحنات للتجربة فقط

    return render(request, 'dashboard.html', {
        'customer': customer,
        'shipments': shipments
    })

# 2. واجهة طلب شحن المحفظة بالحوالة المالية (رفع الوصل)
# قمنا بإزالة @login_required مؤقتاً لغرض الفحص والتشغيل الفوري
def upload_deposit_receipt(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        image = request.FILES.get('receipt_image')
        
        if request.user.is_authenticated:
            customer = CustomerProfile.objects.filter(user=request.user).first()
            if customer:
                WalletDepositRequest.objects.create(
                    customer=customer,
                    amount_requested=amount,
                    payment_method_used=method,
                    receipt_image=image
                )
        return redirect('customer_dashboard')
        
    return render(request, 'upload_receipt.html')

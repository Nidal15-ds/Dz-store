from datetime import date, datetime, time, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from store.models import Category, Order, OrderItem, Product
from .forms import ProductForm

staff_required = user_passes_test(lambda u: u.is_staff, login_url='dashboard:login')


def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:home')

    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard:home')
        error = 'Identifiants invalides.'

    return render(request, 'dashboard/login.html', {'error': error})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('dashboard:login')


@staff_required
def home(request):
    today = timezone.localdate()
    start = timezone.make_aware(datetime.combine(today, time.min))
    end = start + timedelta(days=1)
    orders_today = Order.objects.filter(created_at__gte=start, created_at__lt=end)
    today_income = orders_today.filter(
        status=Order.Status.CONFIRMED
    ).aggregate(total=Sum('total'))['total'] or 0

    context = {
        'active': 'dashboard',
        'orders_today': orders_today.count(),
        'products_count': Product.objects.count(),
        'today_income': today_income,
        'total_orders': Order.objects.count(),
        'pending': Order.objects.filter(status=Order.Status.PENDING).count(),
        'first_call': Order.objects.filter(status=Order.Status.FIRST_CALL).count(),
        'stop_desk': Order.objects.filter(status=Order.Status.STOP_DESK).count(),
        'returned': Order.objects.filter(status=Order.Status.RETURNED).count(),
        'confirmed': Order.objects.filter(status=Order.Status.CONFIRMED).count(),
    }
    return render(request, 'dashboard/index.html', context)


@staff_required
def product_list(request):
    selected_category = request.GET.get('category', '')
    products = Product.objects.select_related('category').order_by('category__id', 'name')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    categories = Category.objects.annotate(product_count=Count('products')).order_by('id')

    return render(request, 'dashboard/products_list.html', {
        'active': 'products',
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })


@staff_required
def product_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:products')
    return render(request, 'dashboard/product_form.html', {
        'active': 'products', 'form': form, 'title': 'Add Product',
    })


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:products')
    return render(request, 'dashboard/product_form.html', {
        'active': 'products', 'form': form, 'title': 'Edit Product',
    })


@staff_required
@require_POST
def product_delete(request, pk):
    Product.objects.filter(pk=pk).delete()
    return redirect('dashboard:products')


@staff_required
def order_list(request):
    status = request.GET.get('status', '')
    q = request.GET.get('q', '').strip()
    orders = Order.objects.prefetch_related('items').all()
    if status:
        orders = orders.filter(status=status)
    if q:
        orders = orders.filter(Q(full_name__icontains=q) | Q(phone__icontains=q))
    return render(request, 'dashboard/orders_list.html', {
        'active': 'orders',
        'orders': orders,
        'statuses': Order.Status.choices,
        'selected_status': status,
        'q': q,
    })


@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items'), pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()
        return redirect('dashboard:order_detail', pk=order.pk)
    return render(request, 'dashboard/order_detail.html', {
        'active': 'orders',
        'order': order,
        'statuses': Order.Status.choices,
    })


@staff_required
def report(request):
    today = timezone.localdate()
    month_param = request.GET.get('month', '')
    year, month = today.year, today.month
    if month_param:
        try:
            year, month = map(int, month_param.split('-'))
        except ValueError:
            year, month = today.year, today.month

    first = date(year, month, 1)
    next_first = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    start = timezone.make_aware(datetime.combine(first, time.min))
    end = timezone.make_aware(datetime.combine(next_first, time.min))

    month_orders = Order.objects.filter(created_at__gte=start, created_at__lt=end)
    confirmed = month_orders.filter(status=Order.Status.CONFIRMED)
    total_revenue = confirmed.aggregate(t=Sum('total'))['t'] or 0

    days_in_month = (next_first - first).days
    daily = []
    for d in range(1, days_in_month + 1):
        day_start = timezone.make_aware(datetime.combine(date(year, month, d), time.min))
        day_end = day_start + timedelta(days=1)
        val = Order.objects.filter(
            status=Order.Status.CONFIRMED,
            created_at__gte=day_start,
            created_at__lt=day_end,
        ).aggregate(t=Sum('total'))['t'] or 0
        daily.append(float(val))

    top_products = list(
        OrderItem.objects.filter(order__in=month_orders)
        .values('product_name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )
    top_products = [
        {'name': item['product_name'], 'quantity': item['total_qty']} for item in top_products
    ]

    context = {
        'active': 'report',
        'month_value': f'{year:04d}-{month:02d}',
        'total_revenue': total_revenue,
        'confirmed_count': confirmed.count(),
        'returned_count': month_orders.filter(status=Order.Status.RETURNED).count(),
        'orders_count': month_orders.count(),
        'labels': list(range(1, days_in_month + 1)),
        'daily': daily,
        'top_products': top_products,
    }
    return render(request, 'dashboard/report.html', context)


@staff_required
def settings_view(request):
    return render(request, 'dashboard/settings.html', {'active': 'settings'})

from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from .models import Category, Product, Wilaya, Order, OrderItem

CATEGORY_ICONS = {
    'qamiss': 'img/icons/qamiss.svg',
    'sport-shoes': 'img/icons/sport-shose.svg',
    't-shirts': 'img/icons/t-shirt.svg',
    'watches': 'img/icons/watch.svg',
    'jackets': 'img/icons/jacket.svg',
    'slacks': 'img/icons/slacks.svg',
    'packs-bundles': 'img/icons/package.svg',
}

FAQS = [
    {'question': 'Do you offer delivery across all 58 Wilayas in Algeria?',
     'answer': 'Yes! We provide reliable home delivery and desk delivery across all 58 wilayas with payment upon receipt (Cash on Delivery).'},
    {'question': 'What is included in the Special Bundle Packs?',
     'answer': 'Our bundle packs combine items like a T-shirt, sport shoes, and a watch together with a special discount (around 7% to 15% off regular prices) to give you a complete outfit match.'},
    {'question': 'Can I exchange or return an item if the size does not fit?',
     'answer': 'Yes, you have up to 48 hours after receiving your package to request a size exchange through our customer support.'},
]


def home(request):
    categories = [
        {'name': c.name, 'slug': c.slug, 'icon': static(CATEGORY_ICONS.get(c.slug, ''))}
        for c in Category.objects.all()
    ]
    return render(request, 'store/home.html', {'categories': categories, 'faqs': FAQS})


def products(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All') or 'All'
    sort = request.GET.get('sort', 'default')

    items = Product.objects.select_related('category').all()
    if q:
        items = items.filter(name__icontains=q)
    if category != 'All':
        items = items.filter(category__name=category)

    if sort == 'low-high':
        items = items.order_by('price')
    elif sort == 'high-low':
        items = items.order_by('-price')
    elif sort == 'rating':
        items = items.order_by('-rating')
    else:
        items = items.order_by('category__id', 'id')

    grouped = {}
    if category == 'All' and not q:
        for c in Category.objects.all():
            cat_items = [p for p in items if p.category_id == c.id]
            if cat_items:
                grouped[c.name] = cat_items

    context = {
        'categories': Category.objects.all(),
        'items': items,
        'grouped': grouped,
        'q': q,
        'selected_category': category,
        'sort': sort,
    }
    return render(request, 'store/products.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def cart(request):
    return render(request, 'store/cart.html')


def checkout(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')

        order = Order.objects.create(
            full_name=request.POST.get('full_name', ''),
            phone=request.POST.get('phone', ''),
            wilaya_id=request.POST.get('wilaya') or None,
            commune=request.POST.get('commune', ''),
            shipping_method=request.POST.get('shipping_method', Order.Shipping.HOME),
        )

        total = 0
        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.filter(pk=pid).first()
            if not product:
                continue
            quantity = int(qty)
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
            )
            total += product.price * quantity

        order.total = total
        order.save()
        return redirect('store:order_success', pk=order.pk)

    return render(request, 'store/checkout.html', {'wilayas': Wilaya.objects.all()})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_success.html', {'order': order})



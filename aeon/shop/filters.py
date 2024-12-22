from shop.models import Brand
def check_filtering(request):
    filters = {}
    ordering = None
    
    title = request.GET.get('search_title')
    low_price = request.GET.get('lp')
    max_price = request.GET.get('mp')

    brands = request.GET.getlist('brand_key')
    
    sort_option = request.GET.get('sort_option')


    try:
        if low_price:
            filters['price__gte'] = float(low_price)
        if max_price:
            filters['price__lte'] = float(max_price)
        if brands:
            brands = Brand.objects.filter(name__in=brands).values_list('id', flat=True)
            filters['brand__in'] = brands
        if title:
            filters['title__icontains'] = title
    except ValueError:
        pass 

    return (filters, sort_option)
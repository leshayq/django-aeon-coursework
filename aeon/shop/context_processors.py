from .models import Category, MenuItem

def get_menu_items(request):
    menu_items = MenuItem.objects.all()

    return {'menu_items': menu_items}
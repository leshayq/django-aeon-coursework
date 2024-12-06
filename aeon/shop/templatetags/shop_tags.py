from django import template
register = template.Library()
from shop.models import ProductProxy, Category

content = {
    'Мобільні телефони': {
        'Смартфони': {
            'Xiaomi': '/mobilni-telefoni/?brand_key=Xiaomi&sort_option=popularity',
            'Apple': '/mobilni-telefoni/?brand_key=Apple&sort_option=popularity',
            'Samsung': '/mobilni-telefoni/?brand_key=Samsung&sort_option=popularity',
            'OPPO': '/mobilni-telefoni/?brand_key=OPPO&sort_option=popularity',
            'Honor': '/mobilni-telefoni/?brand_key=Honor&sort_option=popularity',
            'Всі смартфони': '/mobilni-telefoni/?sort_option=popularity',
        },
        'Аксесуари': {
            'Захисне скло': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=Захисне+скло',
            'Зарядні пристрої': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=зарядний+пристрій',
            'Бездротові зарядки': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=бездротова+зарядка',
            'Адаптери і кабелі': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=кабель&search_title=адаптер&search_title=перехідник',
        },
        'Чохли': {
                'Сумісні з Iphone': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=Чохол+Iphone',
                'Сумісні з Xiaomi': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=Чохол+Xiaomi',
                'Сумісні з Samsung': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=Чохол+Samsung',
                'Всі товари': '/aksesuari-dlya-mobilnih-telefoniv/?sort_option=popularity&search_title=Чохол',
        },
    },
   'Телевізори та мультимедіа': {
        'Телевізори': {
            'Xiaomi': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Samsung': '/mobilni-telefoni/?brand_key=Samsung',
            'LG': '/mobilni-telefoni/?brand_key=Apple',
            'Sony': '/mobilni-telefoni/?brand_key=OPPO',
            'Phillips': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Honor&sort_option=popularity',
            'Всі телевізори': '/mobilni-telefoni/?sort_option=popularity',
        },
        'Фото і відеотехніка': {
            'Фотоапарати': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
            'Об\'єктиви': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
            'Штативи': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
            'Адаптери і кабелі': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
        },
        'Аксесуари': {
                'Приставки Smart TV': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
                'Кронштейни для ТВ': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
                'Кабелі та перехідники': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
                'Мережеві фільтри': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Блок2&sort_option=popularity',
        },
    },
    'Комп\'ютери': {
        'Каталог ПК': {
            'Для офісу': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Для геймінгу': '/mobilni-telefoni/?brand_key=Samsung',
            'Для кіберспорту': '/mobilni-telefoni/?brand_key=Apple',
            'Усі ПК': '/mobilni-telefoni/?brand_key=Apple',
        },
    },
    'Ноутбуки': {
        'Каталог ноутбуків': {
            'Для офісу': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Для геймінгу': '/mobilni-telefoni/?brand_key=Samsung',
            'Для кіберспорту': '/mobilni-telefoni/?brand_key=Apple',
            'Усі ноутбуки': '/mobilni-telefoni/?brand_key=Apple',
        },
    },
    'Периферія': {
        'Маніпулятори': {
            'Миші': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Клавіатури': '/mobilni-telefoni/?brand_key=Samsung',
            'Килимки': '/mobilni-telefoni/?brand_key=Apple',
            'Ігрові маніпулятори': '/mobilni-telefoni/?brand_key=Apple',
        },
        'Аудіотехніка': {
            'Навушники': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Мікрофони': '/mobilni-telefoni/?brand_key=Samsung',
            'Акустичні системи': '/mobilni-telefoni/?brand_key=Apple',
        },
        'Техніка для стримінгу': {
            'Веб-камери': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
        },
    },
   'Геймінг': {
        'Стаціонарні': {
            'Xbox': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Playstation': '/mobilni-telefoni/?brand_key=Samsung',
        },
        'Портативні': {
            'Nintendo': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Steamdeck': '/mobilni-telefoni/?brand_key=Samsung',
        },
        'Аксесуари для консолей': {
            'Геймпади': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'VR': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
            'Кермо для консолі': '/mobilni-telefoni/?search_title=&lp=&mp=&brand_key=Xiaomi&sort_option=popularity',
        },
    },
}


@register.filter
def get_category_content(value):
    try:
        return content[value] 
    except KeyError:
        return None
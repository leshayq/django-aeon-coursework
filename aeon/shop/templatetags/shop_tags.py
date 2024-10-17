from django import template
register = template.Library()

content = {'Мобільні телефони': '<b>Смартфони1 Бебра</b>',
            'Телевізори та мультимедіа': '<i>Телевізори та мультимедіа1 Київ</i>',
            'Комп\'ютери': 'Комп\'ютери1 Рандом',
            'Ноутбуки': 'Ноутбуки1 Слова',
            'Периферія': 'Периферія1 Пишу ',
            'Геймінг': 'Геймінг1 Я'}

@register.filter
def get_category_content(value):
    return content[value]
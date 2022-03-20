from django.conf import settings
static = settings.STATIC_URL

data = {
    'header': {
        'links': [
            {'title': 'О салоне', 'value': 'about'},
            {'title': 'Услуги', 'value': 'services'},
            {'title': 'Наши работы', 'value': 'ourworks'},
            {'title': 'Акции', 'value': 'promo'},
            {'title': 'Отзывы', 'value': 'feedbacks'},
            {'title': 'Контакты', 'value': 'footer'}
        ]
    }
}

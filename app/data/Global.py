from django.conf import settings
static = settings.STATIC_URL

def get_global_data(linkPrefix = ''):
    return {
        'header': {
            'links': [
                {'title': 'О салоне', 'value': f'{linkPrefix}about'},
                {'title': 'Услуги', 'value': f'{linkPrefix}services'},
                {'title': 'Наши работы', 'value': f'{linkPrefix}ourworks'},
                {'title': 'Акции', 'value': f'{linkPrefix}promo'},
                {'title': 'Отзывы', 'value': f'{linkPrefix}feedbacks'},
                {'title': 'Контакты', 'value': f'{linkPrefix}footer'}
            ]
        }
    }

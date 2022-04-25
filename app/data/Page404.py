from .Global import get_global_data


global_data = get_global_data('/#')

data = {
    **global_data,
    'title': 'Страница не найдена',
}

from django import template

register = template.Library()


@register.simple_tag
def custom_pagination(page_obj):
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages
    pagination = []

    if total_pages <= 5:
        pagination = list(range(1, total_pages + 1))
    else:
        if current_page == 1:
            pagination = [1, 2, 3, '...', total_pages]
        elif current_page == total_pages:
            pagination = [1, '...', total_pages - 2, total_pages - 1, total_pages]
        else:
            pagination = [1]
            if current_page > 3:
                pagination.append('...')
            pagination.extend([current_page - 1, current_page, current_page + 1])
            if current_page < total_pages - 2:
                pagination.append('...')
            pagination.append(total_pages)

    return pagination

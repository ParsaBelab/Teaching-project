from django import template
from django.template.defaultfilters import yesno
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def favorite_link(context, post):
    user = context['user']
    if user.is_authenticated:
        is_favorited = post in user.favorites.all()
        url = reverse('Home:toggle_favorite', args=[post.id])
        heart_icon = '❤️' if is_favorited else '🤍'
        return format_html('<a href="{}" class="favorite-link" data-post-id="{}">{}</a>', url, post.id, heart_icon)
    return ''

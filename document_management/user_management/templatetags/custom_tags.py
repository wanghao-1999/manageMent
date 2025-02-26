from django import template

register = template.Library()


@register.filter
def is_superuser(user):
    return user.is_superuser

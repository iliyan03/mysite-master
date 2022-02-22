from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    path = request.path
    if path == pattern:
        return True
    return False

@register.filter
def get_value_in_qs(queryset, key):
    return queryset.values_list(key, flat=True)
from django import template


register = template.Library()

@register.filter(name='range')
def range_filter(value):
    return range(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def startswith(text, starts):
    return str(text).startswith(str(starts))
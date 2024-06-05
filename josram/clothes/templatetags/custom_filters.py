from django import template
import locale

register = template.Library()

@register.filter
def currency(value):
    try:
        # Set locale to US for formatting (or your desired locale)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        # Format with thousands separator and currency symbol
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError):
        return value
    

@register.filter(name='multiply')
def multiply(value1, value2):
    try:
        return value1 * value2
    except (TypeError, ValueError):
        return None
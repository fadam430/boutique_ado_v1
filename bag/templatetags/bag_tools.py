from django import template # looking for django documentation on template tags and filters

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """ Calculate the subtotal for a product in the bag """
    return price * quantity
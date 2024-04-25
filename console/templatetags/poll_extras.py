from django import template

register = template.Library()

# @register.simple_tag()
def multiply(a, b, *args, **kwargs):
    # you would need to do any localization of the result here
    # print('qty*************8', a*b  )
    return a*b


register.filter('multiply',multiply)
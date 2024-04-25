from django import template
register = template.library()

# templates = get.templates()

@register.filter(name='replace')
def replace_text(text,old_value, new_value):
    return text.replace(old_value, new_value)
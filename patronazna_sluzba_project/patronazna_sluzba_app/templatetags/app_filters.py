from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='int_length')
def int_length(number):
    return len(str(number))

@register.filter(name='name_initial')
def name_initial(name):
    try:
        return name[0]
    except:
        return "EMPTY"

@register.filter(name='text_length')
def text_lenght(text):
    return len(text)

@register.filter(name='to_string')
def to_string(text):
    return str(text)
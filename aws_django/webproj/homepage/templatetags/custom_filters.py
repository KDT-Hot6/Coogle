from django import template

register = template.Library()

@register.filter(name='numbering')
def numbering(value):
    number = 6 * (value - 1) + (value - 1)

    return number


@register.filter(name='strCut')
def strCut(value):
    summary = value[:25]

    return summary


@register.filter(name='getButtonId')
def getButtonId(value, arg):
    number = 'button' + str(value) + str(arg)

    return number


@register.filter(name='getResInfo')
def getResInfo(res_list, arg):
    res_info = res_list[arg]

    return res_info
from django import template

register = template.Library()


@register.filter("fullname")
def fullname(user):
    return user.first_name.title() + " " + user.last_name.title()


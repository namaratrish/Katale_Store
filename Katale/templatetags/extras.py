__author__ = 'LT10'
from django import template
from Katale.models import Category

register = template.Library()


@register.inclusion_tag('Katale/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}
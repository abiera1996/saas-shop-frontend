import math
import json
from django import template 
import base64, json, datetime 
from config import settings
from utils import helpers 

register = template.Library()


@register.simple_tag
def format_currency(value, currency_sign='', is_decimal=True):
    """
    Format currency values
    :param value
    :param currency_sign
    :param is_decimal
    :return:
    """
    
    if is_decimal:
        if not value or value is None or value == '':
            value = 0
        formatted_value = math.floor(float(value) * 10 ** 2) / 10 ** 2
        value = currency_sign + " " + "{:,}".format(formatted_value)

    return value

 

@register.simple_tag
def get_time_span(start_date, end_date, type=None):
    if end_date and start_date:
        c = end_date-start_date 
        if type == 'minutes':
            return c.seconds / 60
        elif type == 'days': 
            return int((c.seconds / 60) / 1440)
        else:
            span_string = '' 
            if c.days >= 0:
                if c.days != 0:
                    span_string += str(int(c.days)) + helpers.check_plural(int(c.days), ' day') + ' '

                minutes = divmod(c.total_seconds(), 60)  
                hours = divmod(minutes[0], 60)  

                if type == 'full_format':
                    span_string = ''
                    h = 0
                    if c.days != 0:
                        h = int(c.days) * 24
                    if hours[0] != 0 or h != 0:
                        span_string += str(int(hours[0]) + h) + ':'
                    else:
                        span_string += '0:'

                    if hours[1] != 0:
                        span_string += str(int(hours[1])) + ':'
                    else:
                        span_string += '00:'
                    if minutes[1] != 0:
                        span_string += str(int(minutes[1]))
                    else:
                        span_string += '00'
                else:
                    if hours[0] != 0:
                        span_string += str(int(hours[0])) + helpers.check_plural(int(hours[0]), ' hour') + ' '
                    if hours[1] != 0:
                        span_string += str(int(hours[1])) + helpers.check_plural(int(hours[1]), ' minute') + ' '
                    if minutes[1] != 0:
                        span_string += str(int(minutes[1])) + helpers.check_plural(int(minutes[1]), ' second')
                return  span_string
            return ''
    return ''


@register.simple_tag
def base_url():
    """
    Returns the discount of cart item
    :return:
    """
    

    return settings.BASE_URL 
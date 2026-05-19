"""
Utilities custom filters
"""
import json
import math
from dateutil import parser
from django.utils import formats
from django import template
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def concat_related_name(string1, string2):
    return "%s%s_cfb" % ("%s|" % string1 if string1 != "" and string1 else "", string2)


@register.filter
def loop_range(from_val, to_val):
    return range(int(from_val), int(to_val) + 1)


@register.filter
def as_list(value, separator):
    return value.split(separator)


@register.filter
def moneyfy(val, suffix=""):
    if val:
        val = round(float(val), 2)
        val = "%s%s" % (intcomma(int(val)), ("%0.2f" % val)[-3:])
    else:
        val = "0.00"

    return "%s%s" % (suffix,val)


@register.filter
def commafy(val, show_decimal=False):
    if val:
        val = round(float(val), 2)
        whole = intcomma(int(val))
        decimal = ("%0.2f" % val)[-3:] if show_decimal else ""
        return_val = "%s%s" % (whole, decimal)
    else:
        return_val = "0"

    return return_val


@register.filter
def get_last_active(value):

    if value:
        time_diff = (now() - value).seconds

        if time_diff < 60:
            return "%s %s" % (time_diff, "second(s) ago")
        elif 60 <= time_diff < 3600:
            return "%s %s" % (floor(time_diff / 60), "minute(s) ago")
        elif 3600 <= time_diff < 86400:
            return "%s %s" % (floor(time_diff / 3600), "hour(s) ago")
        elif 86400 <= time_diff < 604800:
            return "%s %s" % (floor(time_diff / 86400), "day(s) ago")
        else:
            return "%s %s" % (floor(time_diff / 604800), "week(s) ago")

    return ""


# @register.filter
# def replace(val, values=""):
#     if values != "":
#         values = values.split("|")
#         val.replace(values[0], values[1])
#     else:
#         return val


@register.filter
def jsonify(data):
    return json.dumps(data)


@register.filter
def format_bool(value, choice_format):
    choices = choice_format.split("|")

    return choices[0] if value else choices[1]


@register.filter
def format_bool_with_count(value, choice_format):
    choices = choice_format.split("|")

    return "%d %s" % (value, choices[0]) if value > 1 else \
        "%d %s" % (value, choices[1]) if value == 1 else "No %s" % choices[1]


@register.filter
def get_initial(value, separator="."):
    return "%s%s" % (value[0], separator) if value and value != "" else ""


@register.filter
def placeholder(value, placeholder_text):
    return placeholder_text if value in ["", None] else value


@register.filter
def censor(value, places=3, code="*"):
    str_val = "%s" % value

    if str_val != "" and len(str_val) >= 3:
        prepend = "".join([code for a in str_val[:-places]])
        return "%s%s" % (prepend, str_val[-places:])

    return str_val


@register.filter
def placeholder_image(image, placeholder_type="image"):
    if placeholder_type not in ('female', 'male', 'image', 'avatar'):
        placeholder_type = 'avatar'
    img_placeholder = "/static/image/%s-placeholder.png" % placeholder_type
    if image:
        if 'http' in image:
            return image
        else:
            return "/media/%s" % image 
    else:
        return img_placeholder

    


@register.filter
def deduct(value1, value2):
    return float(value1) - float(value2)


@register.filter
def times(value1, value2):
    return float(value1) * float(value2)


@register.filter
def divide(value1, value2):
    return float(value1) / float(value2)


@register.filter
def get_int_sum_of_key(array, key):
    return int(sum(list(map(float, [item[key] for item in array]))))


@register.filter
def get_float_sum_of_key(array, key):
    return sum(list(map(float, [item[key] for item in array])))


@register.filter
def floor(amount):
    return math.floor(float(amount))


@register.filter
def ceil(amount):
    return math.ceil(float(amount))


@register.filter
def replace(val1, val2):
    values = val2.split("|")
    return val1.replace(values[0], values[1])


@register.filter
def in_list(val1, val2):
    if type(val2) is str:
        val2 = val2.split("|")
    return val1 in val2


@register.filter
def in_array(value, lookup):
    """
    check if value is in array
    :return:
    """

    return value in lookup


@register.filter
def get_category(categories=[]):
    value = "None"
    values = []

    if len(categories) > 0:
        for category in categories:
            values.append(category['name'])

        value = ",".join(values)

    return value


@register.filter
def cus_datetime_from_timezone(tzs, option="full"):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    try:
        tzs = tzs.split("T")
        date = list(map(int, tzs[0].split("-")))
        time = tzs[1].split(":") if len(tzs) >= 2 else ""

        if option == "date":
            return "%s. %s, %s " % (months[date[1]], date[2], date[0])

        elif option == "time":
            hour = int(time[0])
            minute = int(time[1])

            suffix = "am" if hour < 12 or hour == 24 else "pm"
            hour = hour - 12 if hour > 12 else hour

            return "%s:%s %s" % (hour, minute, suffix)

        else:
            date_time_data = ["%s. %s, %s" % (months[date[1]], date[2], date[0])]

            if time != "":
                hour = int(time[0])
                minute = int(time[1])

                suffix = "am" if hour < 12 or hour == 24 else "pm"
                hour = hour - 12 if hour > 12 else hour

                date_time_data.append("%s:%s %s" % (hour, minute, suffix))

            return " - ".join(date_time_data)

    except:
        return "N/A"


@register.filter
def cus_timezone_date_to_date(tzs, option="full"):
    try:
        date = parser.parse(tzs)
        if option == "full":
            return date.strftime("%b. %d, %Y %H:%M %p")
        elif option == "date":
            return date.strftime("%b. %d, %Y")
        elif option == "time":
            return date.strftime("%H:%M %p")
    except:
        return "N/A"


@register.filter
def get_sum_of_key(array, key=''):
    try:
        return sum([int(item[key]) for item in array])
    except:
        return 0


@register.filter
def to_int(val):
    return int(val)


@register.filter
def to_str(value):
    return str(value)


@register.filter
def custom_date(value, date_format="%m-%d-%Y %H:%M:%S"):
    try:
        datetime_object = datetime.strptime(value, date_format)

        strf_format = "%b. %e, %Y"
        if "%H:%M:%S" in date_format:
            strf_format = "%b. %e, %Y - %l:%M %p"

        return datetime_object.strftime(strf_format)

    except Exception as ex:
        print(ex.args[0])
        return ""


@register.filter
def custom_date_only(value, date_format="%m-%d-%Y"):
    try:
        datetime_object = datetime.strptime(value, date_format)

        strf_format = "%b. %e, %Y"
        if "%H:%M:%S" in date_format:
            strf_format = "%b. %e, %Y - %l:%M %p"

        return datetime_object.strftime(strf_format)

    except Exception as ex:
        print(ex.args[0])
        return ""


@register.filter
def format_date(value, date_format="%m-%d-%Y %H:%M:%S"):
    try:
        datetime_object = datetime.strptime(value, "%m-%d-%Y %H:%M:%S")
        return datetime_object.strftime(date_format)

    except Exception as ex:
        print(ex.args[0])
        return ""


@register.filter
def set_preparation_date(value, days=0):
    try:
        datetime_object = datetime.strptime(value, "%m-%d-%Y %H:%M:%S")
        return (datetime_object + timedelta(days=days)).strftime("%m-%d-%Y")

    except Exception as ex:
        print(ex.args[0])
        return ""


@register.filter
def get_options(value):
    options = []

    for option in value.options.all():
        options.append({
            'label': option.label,
            'value': option.value
        })

    x = json.dumps(options)
    return x


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)
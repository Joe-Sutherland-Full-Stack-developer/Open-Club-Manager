from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def get_instance(instances, day, time):
    for instance in instances:
        if instance.day == day and instance.start_time.strftime('%H:%M') == time:
            return instance
    return None

@register.filter
def subtract(value, arg):
    return value - arg



@register.filter
def get_item(list_or_dict, index):
    if isinstance(list_or_dict, dict):
        return list_or_dict.get(index)
    elif isinstance(list_or_dict, (list, tuple)):
        return list_or_dict[index] if 0 <= index < len(list_or_dict) else None
    return None

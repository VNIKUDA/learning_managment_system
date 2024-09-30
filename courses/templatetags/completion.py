from django.template import Library

register = Library()

@register.filter(name="get_completion")
def get_completion(completions, user):
    return completions.get(student=user)

@register.filter(name="endswith")
def endswith(value, args):
    return any(value.lower().endswith(arg.lower()) for arg in args.split())
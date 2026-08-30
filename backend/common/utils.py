def display_code(instance, field_name):
    return getattr(instance, field_name, str(instance.pk))

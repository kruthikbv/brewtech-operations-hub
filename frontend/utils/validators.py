def required(value, label):
    if not str(value or '').strip(): raise ValueError(f'{label} is required.')

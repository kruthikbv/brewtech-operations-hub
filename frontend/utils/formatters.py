def as_records(payload):
    return payload.get('results', []) if isinstance(payload, dict) else payload

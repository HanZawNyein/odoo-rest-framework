def report_domain_serialize(data):
    remove_field = {'lang', 'tz', 'uid', 'allowed_company_ids', 'active_model', 'active_id', 'active_ids', 'context'}
    fields = list(set(list(data.keys())) - remove_field)
    result = []
    for d in fields:
        if data.get(d):
            try:
                result.append((d, '=', int(data.get(d))))
            except:
                result.append((d, '=', data.get(d)))
        continue
    return result

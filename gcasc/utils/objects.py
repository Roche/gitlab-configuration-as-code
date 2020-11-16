def update_object(current, new, prefix=""):  # type: (dict, dict, str)->int
    for key, value in new.items():
        if isinstance(value, dict):
            update_object(current, value, "{0}{1}_".format(prefix, key))
            continue

        prefixed_key = "{0}{1}".format(prefix, key)
        if hasattr(current, prefixed_key):
            current_value = getattr(current, prefixed_key)
            if current_value != value:
                setattr(current, prefixed_key, value)

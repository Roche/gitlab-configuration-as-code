class DiffResult:
    def __init__(self, create, update, remove, unchanged):
        self.create = create
        self.update = update
        self.remove = remove
        self.unchanged = unchanged

    def has_changes(self):
        return len(self.create) > 0 or len(self.update) > 0 or len(self.remove) > 0


def diff_list(list1, list2, keys=None):
    if isinstance(keys, str):
        keys = [keys]
    list1_dict = to_map(list1, keys)
    list2_dict = to_map(list2, keys)
    return __compare(list1_dict, list2_dict)


def to_map(list, keys):
    if keys is None or len(keys) == 0:
        # all fields are keys, so no mapping
        return list
    key_function = (
        (lambda obj: obj[keys[0]])
        if len(keys) == 1
        else (lambda obj: create_tuple_key(obj, keys))
    )
    return {key_function(_unwrap_object(obj)): obj for obj in list}


def _unwrap_object(obj):
    unwrapped = obj if isinstance(obj, dict) else obj.__dict__
    # python-gitlab object props are wrapped in _attrs, so we should unwrap
    return unwrapped if "_attrs" not in unwrapped else unwrapped["_attrs"]


def _filter_non_primitive(obj):
    return dict(filter(lambda tuple: _is_primitive(tuple[1]), obj.items()))


def _is_primitive(obj):
    return type(obj) in (int, str, bool, list, dict, tuple)


def create_tuple_key(obj, keys):
    return tuple(map(lambda key: obj.get(key), keys))


def __compare(obj1, obj2):
    create = []
    update = []
    unchanged = []

    for key, value in obj1.items():
        value2 = obj2.get(key)
        if value2 is None:
            create.append(value)
        else:
            if __compare_single(value, value2):
                unchanged.append(value)
            else:
                update.append((value, value2))
            del obj2[key]
    remove = list(obj2.values())

    return DiffResult(create, update, remove, unchanged)


def __compare_single(obj1, obj2):
    obj2_unwrapped = _unwrap_object(obj2)
    for attr, value in obj1.items():
        if obj2_unwrapped[attr] != value:
            return False
    return True

import pytest

from gcasc.utils import diff

KEY = "key"


class MyObject:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def save(self):
        return self.key


def _create_list(key, value, additional=None):
    obj = {KEY: key, "value": value}
    if not additional is None and isinstance(additional, dict):
        obj = {**obj, **additional}
    return [obj]


def test_diff_created():
    # given
    list1 = _create_list("a", "b")
    list2 = []

    # when
    result = diff.diff_list(list1, list2, KEY)

    # then
    _assert_diff_result(result, create=1)
    assert result.create[0] == list1[0]


@pytest.mark.parametrize(
    "value",
    [
        ("b", "c"),  # string
        (1, 2),  # int
        (1.1, 2.2),  # float
        (True, False),  # bool
        ([1, 1], [1, 2]),  # list(number)
        (["a", "a"], ["a", "a", "c"]),  # list(string)
        (("a", 1), ("b", 1)),  # tuple
        ({"x": "y"}, {"x": "z"}),  # dict
        ({"x": {"y": 1}}, {"x": {"y": 2}}),  # nested dict
    ],
)
def test_diff_updated_primitive(value):
    # given
    list1 = _create_list("a", value[0])
    list2 = _create_list("a", value[1])

    # when
    result = diff.diff_list(list1, list2, KEY)

    # then
    _assert_diff_result(result, update=1)
    assert result.update[0] == (list1[0], list2[0])


def test_diff_removed():
    # given
    list1 = []
    list2 = _create_list("a", "b")

    # when
    result = diff.diff_list(list1, list2, KEY)

    # then
    _assert_diff_result(result, remove=1)
    assert result.remove[0] == (list2[0])


def test_diff_unchanged():
    # given
    list1 = _create_list("a", "a", additional={"c": 1, "d": [1]})
    list2 = _create_list("a", "a", additional={"c": 1, "d": [1]})

    # when
    result = diff.diff_list(list1, list2, KEY)

    # then
    _assert_diff_result(result, unchanged=1)
    assert result.unchanged[0] == (list1[0])


@pytest.mark.parametrize(
    "list2",
    [
        _create_list("a", "a", {"save": (lambda x: x)}),
        [MyObject("a", "a")],
        _create_list("a", "a", {"save": MyObject("a", "a")}),
    ],
)
def test_diff_discards_complex_values(list2):
    # given
    list1 = _create_list("a", "a")

    # when
    result = diff.diff_list(list1, list2, KEY)

    # then
    _assert_diff_result(result, unchanged=1)
    assert result.unchanged[0] == (list1[0])


def test_diff_on_multiple_keys():
    # given
    list1 = [
        {KEY: "a", "key2": 1, "value": 1},
        {KEY: "b", "key2": "a", "value": 1},
        {KEY: "c", "key2": 1, "value": 1},
        {KEY: "e", "key2": 2, "value": 1},
    ]
    list2 = [
        {KEY: "a", "key2": 1, "value": 1},
        {KEY: "b", "key2": "a", "value": 2},
        {KEY: "c", "key2": 2, "value": 1},
        {KEY: "d", "key2": 2, "value": 1},
    ]

    # when
    result = diff.diff_list(list1, list2, [KEY, "key2"])

    # then
    _assert_diff_result(result, create=2, update=1, remove=2, unchanged=1)


def _assert_diff_result(result, create=0, update=0, remove=0, unchanged=0):
    assert len(result.create) == create
    assert len(result.update) == update
    assert len(result.remove) == remove
    assert len(result.unchanged) == unchanged

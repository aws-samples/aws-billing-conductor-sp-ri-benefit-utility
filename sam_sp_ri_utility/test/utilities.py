def is_equal_list_of_dict(actual, expected):
    return [item for item in actual if item not in expected] == [] and [item for item in expected if
                                                                        item not in actual] == []

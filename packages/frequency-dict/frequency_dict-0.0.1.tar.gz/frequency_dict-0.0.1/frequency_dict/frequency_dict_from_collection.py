def frequency_dict_from_collection(collection):
    """
    This is a useful function to convert a collection of items into a dictionary depicting the frequency of each of
    the items. :param collection: Takes a collection of items as input :return: dict
    """
    assert len(collection) > 0, "Cannot perform the operation on an empty collection"
    dictionary = {}
    keys = []
    for item in collection:
        if item not in keys:
            keys.append(item)
            dictionary[item] = 0
        dictionary[item] += 1
    return dictionary

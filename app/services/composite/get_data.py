def get_paginated_results(data, url, start: int, limit: int):

    output = {}
    if len(data) == 0:
        output["result"] = data
        output["next"] = ""
        output["previous"] = ""
        return output

    if not isinstance(data, list):  # if the data is not in the form of a list then make it as list
        data = [data]

    output = {
        "start": start,
        "limit": limit,
        "count": len(data),
    }

    if start + limit >= len(data):
        output["next"] = ""
    else:
        output["next"] = "{0}?offset={1}&limit={2}".format(url, start + limit, limit)

    if start - limit < 0:
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, 0, limit)
    elif start > len(data):
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, len(data) - limit, limit)
    else:
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, start - limit, limit)

    output["results"] = data[start:start + limit]
    return output
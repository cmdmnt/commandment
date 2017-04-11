from .commands import DeviceInformation


def queryresponses_to_query_set(responses: dict):
    return {DeviceInformation.Queries(k): v for k, v in responses.items()}

from cubic.rest import Rest


class FileClient:
    __rest: Rest
    __server: str
    __user: dict
    __token_key: str

    def __init__(self, server: str, user: dict, token_key: str):
        self.__server = server
        self.__user = user
        self.__token_key = token_key
        self.__rest = Rest(server=self.__server)

    def list(self, home_type: str, path: str = "/", sort: str = "NAME_ASC", ext_filters: set = {}):
        filter_regex = ""
        if len(ext_filters) > 0:
            filter_regex = ".*\\.(" + "|".join({x.lower() for x in ext_filters}) + ")$"

        # print("filter_regex", filter_regex)

        return self.__rest.post("files", {
            'user': self.__user,
            'tokenKey': self.__token_key,
            'home': home_type,
            'path': path,
            'sort': sort,
            'nameFilterRegex': filter_regex
        })

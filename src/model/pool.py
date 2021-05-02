class Pool:
    pools = dict()

    def __init__(self, id, values):
        self.__id = id
        self.__values = values

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_values(self):
        return self.__values.copy()

    def set_values(self, values):
        self.__values = values

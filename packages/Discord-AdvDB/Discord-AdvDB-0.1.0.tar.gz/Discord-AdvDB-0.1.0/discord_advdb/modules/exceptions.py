class TableAlreadyExists(Exception):

    def __init__(self, message="Table already exists in the database"):
        self.message = message
        super().__init__(self.message)


class ColumnDoesNotExist(Exception):

    def __init__(self, message="Column for the key column does not exist!"):
        self.message = message
        super().__init__(self.message)


class TableDoesNotExist(Exception):

    def __init__(self, message="Table does not exist in the database"):
        self.message = message
        super().__init__(self.message)


class NonEqualEntryException(Exception):

    def __init__(self, message="Entry values and columns mismatched"):
        self.message = message
        super().__init__(self.message)


class OptionTypeError(Exception):

    def __init__(self, message="A column can't have two types!"):
        self.message = message
        super().__init__(self.message)


class EntryTypeNotColumnType(Exception):

    def __init__(self, value):
        self.value = value
        self.message = f"The value {self.value} is not the same type as the column"
        super().__init__(self.message)


class EntryHasNoType(Exception):

    def __init__(self):
        self.message = "Entry has no Type ( INT, STR OR FLOAT )"
        super().__init__(self.message)


class KeyAlreadyExists(Exception):

    def __init__(self):
        self.message = "The key entered for the entry already exists"
        super().__init__(self.message)

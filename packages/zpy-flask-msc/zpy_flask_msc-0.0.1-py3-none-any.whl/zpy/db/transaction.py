from enum import Enum


class ZOperation(Enum):
    INSERT = "INSERT"  # Insert that return nre id
    UPDATE = "UPDATE"  # Update that return row before updated
    DELETE = "DELETE"  # Delete return row deleted
    INT_INSERT = "IN_INSERT"  # Insert that return row with data inserted
    INT_UPDATE = "IN_UPDATE"  # Update that return row with data inserted
    INT_DELETE = "IN_DELETE"  # Delete return row with data inserted


class ZTranstaction(object):

    default_transaction: str = "default"
    store = None

    def __init__(self) -> None:
        super().__init__()
        self.store = {self.default_transaction: {}}

    def begin_txn(self, name: str):
        self.store[name] = {}

    def operation(
        self, operation: ZOperation, table: str, data: dict, transaction: str = None
    ):
        transact = transaction or self.default_transaction
        operation = {"type": operation.value, "data": data}
        if table in self.store[transact]:
            self.store[transact][table].append(operation)
        else:
            self.store[transact][table] = [operation]

    def insert(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.INSERT, table, data, transaction)

    def update(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.UPDATE, table, data, transaction)

    def delete(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.DELETE, table, data, transaction)

    def int_insert(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.INT_INSERT, table, data, transaction)

    def int_update(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.INT_UPDATE, table, data, transaction)

    def int_delete(self, table: str, data: dict, transaction: str = None):
        self.operation(ZOperation.INT_DELETE, table, data, transaction)

    def commit(self, name: str = None, pop: bool = False):
        print(self.store)
        transact = name
        if name not in self.store or name == None:
            transact = self.default_transaction
        if pop:
            return self.store.pop(transact, None)
        return self.store[transact]
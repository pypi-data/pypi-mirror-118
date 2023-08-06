import uuid


class BaseClass:
    def __init__(self, name, *args, **kwargs):
        self.uuid = uuid.uuid4()
        self.name = name


class Controller(BaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Stateful(BaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

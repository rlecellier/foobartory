import uuid


class BaseProduct():
    def __init__(self):
        self.id = uuid.uuid4()


class Foo(BaseProduct):
    pass


class Bar(BaseProduct):
    pass


class FooBar(BaseProduct):
    def __init__(self, product_foo, product_bar):
        self.product_foo = product_foo
        self.product_bar = product_bar
        self.serial_number = f'{product_foo.id}_{product_bar.id}'
        super().__init__()

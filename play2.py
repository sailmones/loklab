a =32
class Foo:
    pass
obj = Foo()
class Bar(Foo):
    pass
obj2 = Bar()
print(type(Foo()))

def new(cls):
    x = type.__new__(cls)
    x.attr = 100
    return x

v = new()
print(v.attr)
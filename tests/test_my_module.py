from src.my_module import MyClass


def test_importing():
    cls_instance = MyClass()
    assert cls_instance.say_hello()

""" JSON objects for compare """


def fib(n):
    if n == 0:
        return False
    if n == 1:
        return True
    return {"first": fib(n - 1), "second": fib(n - 2)}


def obj_list(l):
    return [{"text": "Foo", "id": i, "list": []} for i in range(l)]


def num_list(l):
    return list(range(l))


def generate():
    yield ("true", True)
    yield ("false", False)
    yield ("null", None)
    yield ("number", 42)
    yield ("string", 'I hate using \\ to write \"')

    for i in range(0, 16, 2):
        yield ("Fib " + str(i), fib(i))

    for i in [0, 1, 5, 10, 50, 100]:
        yield ("ObjList " + str(i), obj_list(i))

    for i in [0, 1, 5, 10, 50, 100, 1000, 10000]:
        yield ("NumList " + str(i), num_list(i))




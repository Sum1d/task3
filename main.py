import time
from opcua import Server


if __name__ == "__main__":
    server = Server()

    url = "opc.tcp://192.168.0.8:4840"
    server.set_endpoint(url)

    objects = server.get_objects_node()
    ns = server.register_namespace("Server")
    tags = objects.add_object(ns, "Tags")

    # Создание переменных, хранящихся на сервере
    tag1 = tags.add_variable(ns, "First tag", 5)
    tag2 = tags.add_variable(ns, "Second tag", 7)
    tag3 = tags.add_variable(ns, "Third tag", 12)
    counter = tags.add_variable(ns, "Counter", 0)

    c = 0

    tag1.set_writable()
    tag2.set_writable()
    tag3.set_writable()

    server.start()

    while True:
        c += 1
        counter.set_value(c)

        time.sleep(1)

    server.stop()

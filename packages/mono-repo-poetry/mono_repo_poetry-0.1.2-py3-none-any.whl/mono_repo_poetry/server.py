import time


def start_server():
    """
    :return: None
    """
    print("String server @", time.time())
    x = input("Enter done to exit")
    if x == "done":
        exit(0)


if __name__ == "__main__":
    print("In main method")
    start_server()
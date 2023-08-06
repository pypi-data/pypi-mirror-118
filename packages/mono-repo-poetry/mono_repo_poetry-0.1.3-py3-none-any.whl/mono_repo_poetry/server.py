import time


def start_server():
    """
    :return: None
    """
    print("String server @", time.time())
    while True:
        x = input("Enter d to exit")
        if x == "d":
            break
        else:
            print("You just entered: ", x)


if __name__ == "__main__":
    print("In main method")
    start_server()
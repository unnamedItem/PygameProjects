EXIT_STAGE = False

def stage(func):
    def wrapper():
        print("Stage [", func.__name__, "] is running")
        running: bool = True
        while running or running == None:
            running = func()
    return wrapper

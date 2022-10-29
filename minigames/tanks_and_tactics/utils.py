def stage(func):
    print('Stage [', func.__name__, '] is running')
    def wrapper():
        running = True
        while running or running == None:
            running = func()
    return wrapper
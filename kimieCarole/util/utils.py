import time

regex_list = ['+', '-', '*', '/', '%']
number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
def timer(func):
    def counter(*args):

        delay = 0.0000000001
        first_time = time.time()
        result = func(*args)
        time.sleep(delay)
        local_time_consume = (time.time() - first_time - delay) * 1000
        print(('@ ' + func.__name__ + 'time used: %.2f mili sec') % local_time_consume)
        return result

    return counter

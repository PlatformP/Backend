from time import perf_counter


def runtime(func):
    '''
    wrapper which times how long a function takes to run
    :param func:
    :return:
    '''
    def wrap(*args, **kwargs):
        tic = perf_counter()
        result = func(*args, **kwargs)
        toc = perf_counter()
        print(f'Execution time {toc - tic} seconds')
        return result

    return wrap

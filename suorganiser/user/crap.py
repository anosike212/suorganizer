# import logging
# logger = logging.getLogger()
# print(logger.warning())

def test(**kwargs):
    print('error: {0.__class__.__name__}\n'
          'args: {0.args}\n'.format(kwargs['error']))

# my_error = None
try:
    print([4, 8][2])
except Exception as error:
    global my_error
    my_error = error

test(error = my_error)

def test2(**kwargs):
    print(kwargs)
    print("test: {r.count}".format(r = kwargs['crap']))

test2(crap = [3, 5])
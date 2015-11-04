
import collections


def f(schema, data, arr_size=1, bit=0):
    stack = [[schema, iter(schema), arr_size]]
    while True:
        cur_schema_item = next(stack[-1][1])


if __name__ == '__main__':
    schema = (('a', 1, 2), ('b', 2, 0),
              ('c', (('ca', (('caa', 3, 1), ('cab', 2, 0), ('cac', 1, 1)), 2), ('cb', 1, 1)), 3),
              ('d', 2, 2), ('e', 1, 0),
              ('f', (('fa', 2, 1),), 1),
              ('g', (('ga', 2, 1), ('gb', (('gba', (('gbaa', 2, 2),), 1),), 2)), 1))
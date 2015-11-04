
import collections


def f(schema, data, arr_size=1, bit=0):
    TOP = -1
    ITER = 1
    stack = []
    if arr_size:
        stack = [[schema, iter(schema), arr_size]]
    #  2-й элемент списка для отслеживания текущей позиции на разных уровнях иерархии
    #  если 3-й элемент (размер массива) отличен от 1, то 1-й элемент используется для
    #  получения итератора во второй и последующие проходы.
    names = ['/']
    while stack:
        try:
            cur_schema_item = next(stack[TOP][ITER])

            names.append(cur_schema_item[0])
            if isinstance(cur_schema_item[1], int):
                #  DO IT
                print('.'.join(names), cur_schema_item[1], cur_schema_item[2])
                names.pop()
            else:
                print('.'.join(names), cur_schema_item[2])
                if cur_schema_item[2] != 0:
                    stack.append([cur_schema_item[1],
                                  iter(cur_schema_item[1]),
                                  cur_schema_item[2]])
        except StopIteration:
            if stack[TOP][2] > 1:
                stack[TOP][2] -= 1
                stack[TOP][ITER] = iter(stack[TOP][0])
            else:
                stack.pop()
                names.pop()


if __name__ == '__main__':
    schema = (('a', 1, 2), ('b', 2, 0),
              ('c', (('ca', (('caa', 3, 1), ('cab', 2, 0), ('cac', 1, 1)), 2), ('cb', 1, 1)), 3),
              ('d', 2, 2), ('e', 1, 0),
              ('f', (('fa', 2, 1),), 1),
              ('g', (('ga', 2, 1), ('gb', (('gba', (('gbaa', 2, 2),), 1),), 2)), 1))

    f(schema, None)


import collections


TOP = -1
ITER = 0
RESULT = 1
QUANTITY = 2
SCHEME = 3
LST = 4


def f(scheme, data, counter=1, bit=0):

    result = collections.OrderedDict()
    lst = list()
    stack = []

    if counter != 0:
        if counter != 1:
            lst.append(result)
        stack.append([iter(scheme), result, counter - 1, scheme, lst])

    while stack:
        try:
            name, type_, quantity = next(stack[TOP][ITER])

            if quantity == 0:
                print(name, type(type_))
                continue

            if isinstance(type_, int):
                if quantity == 1:
                    val = type_ + 100
                else:
                    val = []
                    # заполнение res
                stack[TOP][RESULT].update({name: val})
            else:
                val_dict = collections.OrderedDict()
                if quantity == 1:
                    stack[TOP][RESULT].update({name: val_dict})
                    stack.append([iter(type_), val_dict, 0])
                else:
                    val_lst = list()
                    val_lst.append(val_dict)
                    stack[TOP][RESULT].update({name: val_lst})
                    stack.append([iter(type_), val_dict, quantity - 1,  type_, val_lst])
                    # raise StopIteration ???

        except StopIteration:
            if stack[TOP][QUANTITY] != 0:
                if stack[TOP][QUANTITY] > 0:
                    stack[TOP][QUANTITY] -= 1
                val_dict = collections.OrderedDict()
                stack[TOP][LST].append(val_dict)
                stack[TOP][RESULT] = val_dict
                stack[TOP][ITER] = iter(stack[TOP][SCHEME])
            else:
                stack.pop()

    return lst if lst else result


if __name__ == '__main__':
    import pprint

    sschema = (
            ('a', 1, 1),
            ('b', (('ba', 2, 2),), 3),
            ('c', 3, 0),
            ('d', (('da', 4, 1),
                   ('db', 5, 1),
                   ('dc', (('dca', 6, 0), ('dcb', 7, 2), ('dcc', 8, 1)), 2),
                   ('dd', 9, 1)), 2)
    )

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(f(sschema, None, 2))

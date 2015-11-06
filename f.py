
import collections
import pprint

TOP = -1
NAME = ITER = 0
SCHEMA = TYPE = 1
CNT = 2
RESULT = 3


def f(scheme, data, length=1, bit=0):

    result = collections.OrderedDict()
    lstt = None
    stack = []

    if length != 0:
        if length != 1:
            lstt = list()
            lstt.append(result)
        stack.append([iter(scheme), scheme, length - 1, result, lstt])

    while stack:
        try:
            name, type_, quantity = next(stack[TOP][ITER])

            if quantity == 0:
                print(name, type(type_))
                continue

            if isinstance(type_, int):
                if quantity == 1:
                    res = type_ + 100
                else:
                    res = []
                    # заполнение res
                stack[TOP][RESULT].update({name: res})
            else:
                if quantity == 1:
                    res = collections.OrderedDict()
                    stack[TOP][RESULT].update({name: res})
                    stack.append([iter(type_), type_, quantity - 1, res, None])
                else:
                    lst = list()
                    res = collections.OrderedDict()
                    lst.append(res)
                    stack[TOP][RESULT].update({name: lst})
                    stack.append([iter(type_), type_, quantity - 1, res, lst])

        except StopIteration:
            if stack[TOP][CNT] != 0:
                if stack[TOP][CNT] > 0:
                    stack[TOP][CNT] -= 1
                # if stack[TOP][4]:
                res = collections.OrderedDict()
                stack[TOP][4].append(res)
                stack[TOP][RESULT] = res
                stack[TOP][ITER] = iter(stack[TOP][SCHEMA])
            else:
                stack.pop()

    return lstt if lstt else result


if __name__ == '__main__':
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


import collections
import pprint

TOP = -1
NAME = ITER = 0
SCHEMA = TYPE = 1
CNT = 2
RESULT = 3

schema = (
        ('a', 1, 1),
        ('b', (('ba', 2, 2),), 1),
        ('c', 3, 0),
        ('d', (('da', 4, 1),
               ('db', 5, 1),
               ('dc', (('dca', 6, 0), ('dcb', 7, 2), ('dcc', 8, 1)), 1),
               ('dd', 9, 1)), 1)
)

result = collections.OrderedDict()

stack = [[iter(schema), schema, 0, result]]


while stack:
    try:
        cur_si = next(stack[TOP][ITER])

        if cur_si[CNT] == 0:
            print(cur_si[NAME], type(cur_si[TYPE]))
            continue

        if isinstance(cur_si[TYPE], int):
            if cur_si[CNT] == 1:
                res = cur_si[TYPE] + 100
            else:
                res = []
                # заполнение res
            stack[TOP][RESULT].update({cur_si[NAME]: res})
        else:
            res = collections.OrderedDict()
            stack[TOP][RESULT].update({cur_si[NAME]: res})
            stack.append([iter(cur_si[TYPE]), cur_si[TYPE], cur_si[CNT]-1, res])

    except StopIteration:
        if stack[TOP][CNT] != 0:
            if stack[TOP][CNT] > 0:
                stack[TOP][CNT] -= 1
            stack[TOP][ITER] = iter(stack[TOP][SCHEMA])
        else:
            stack.pop()


pp = pprint.PrettyPrinter(indent=2)
pp.pprint(result)
# pp.pprint(schema)


def f(L):
    L.append(8)

l = []
f(l)
f(l)
# print(l)
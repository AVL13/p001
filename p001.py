import base64
import xml.dom.minidom
import struct
import collections


class F4M():
    def __init__(self, file):
        # super
        dom = xml.dom.minidom.parse( file )

        bootstrapInfoElement = dom.getElementsByTagName( 'bootstrapInfo' )[0]
        bootstrapInfoEncoded = bootstrapInfoElement.childNodes[0].data.strip( )

        bootstrapInfo = base64.b64decode( bootstrapInfoEncoded )
        self.bsi = bootstrapInfo


dick = { 'SI8': 'b', 'UI8': 'B', 'SI16': '>h', 'UI16': '>H',
         'SI32': '>i', 'UI32': '>I', 'SI64': '>q', 'UI64': '>Q' }


def f(scheme, data):
    ordered_dict = collections.OrderedDict()
    current_bit = 0
    for v in scheme:
        if len(v) == 2:  # Type
            if 1 != len(v[1]):
                raise Exception('Invalid Type specification for ' + v[0])
            if isinstance(v[1][0], tuple):
                ordered_dict[v[0]] = f(v[1][0], data)
            elif isinstance(v[1][0], str):
                ordered_dict[v[0]] = v[1][0]
            else:
                raise Exception('Invalid Type specification for ' + v[0])
        elif len(v) == 3:  # (Type & Size) or (Type & Cond)
            if isinstance(v[2], str):
                if 1 != len(v[1]):
                    raise Exception('Incorrect Type specification for ' + v[0])
                if isinstance(v[1][0], tuple):
                    ordered_dict[v[0]] = f(v[1][0], data)  # Size ??
                elif isinstance(v[1][0], str):
                    ordered_dict[v[0]] = v[1][0]
                else:
                    raise Exception('Invalid Type specification for ' + v[0])
            elif isinstance(v[2], tuple):
                pass
            else:
                raise Exception('Invalid Size or Condition field for ' + v[0])
        elif len(v) == 4:  # Type & Cond & Size
            pass
        else:
            raise Exception('Incorrect specification for ' + v[0])

    named_tuple = collections.namedtuple( 'Box', ' '.join(ordered_dict.keys()) )
    return named_tuple(*[x for x in ordered_dict.values()])


if __name__ == '__main__':
    BOXHEADER = (('TotalSize', ('UI32',)),
                 ('BoxType', ('4CC',)),
                 ('ExtendedSize', ('UI64', None), ('TotalSize', '==', 1))
    )
    AFRAENTRY = (('Time', ('UI64',)),
                 ('Offset', ('UI32', 'UI64',), ('LongOffsets', '==', 0))
    )
    GLOBALAFRAENTRY = (('Time', ('UI64',)),
                       ('Segment', ('UI16', 'UI32'), ('LongIDs', '==', 0)),
                       ('Fragment', ('UI16', 'UI32'), ('LongIDs', '==', 0)),
                       ('AfraOffset', ('UI32', 'UI64'), ('LongOffsets', '==', 0)),
                       ('OffsetFromAfra', ('UI32', 'UI64'), ('LongOffsets', '==', 0), 'fuck')
                      )
    afra = (('Header', (BOXHEADER,)),
            ('Version', ('UI8',)),
            ('Flags', ('UI24',)),
            ('LongIDs', ('UI1',)),
            ('LongOffsets', ('UI1',)),
            ('GlobalEntries', ('UI1',)),
            ('Reserved', ('UI5',)),
            ('TimeScale', ('UI32',)),
            ('EntryCount', ('UI32',)),
            ('LocalAccessEntries', (AFRAENTRY,), 'EntryCount'),
            ('GlobalEntryCount', ('UI32', None), ('GlobalEntries', '==', 1)),  # Nono -> 0
            ('GlobalAccessEntries', (GLOBALAFRAENTRY, None), ('GlobalEntries', '==', 1), 'GlobalEntryCount')
           )
    fh = open('2b5c249bf7bc4904aca37b3e0dfffd7e.mp4.f4m.xml')
    f4m = F4M(fh)
    # print(f4m.bsi)

    print(f(afra, None))

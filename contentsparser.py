import collections


class TimeRep(object):
    def __init__(self, timestr):
        self.__ts = timestr
        h, m = self.__ts.split(':')
        assert h.isdigit()
        assert m.isdigit()
        self.__ti = int(h) * 60 + int(m)

    def asint(self):
        return self.__ti

    def __str__(self):
        return self.__ts


ProgramDescription = collections.namedtuple(
    'ProgramDescription',
    ['channel', 'start_time', 'summary']
    )


def element2description(element):
    try:
        time_element = element.find_element_by_class_name('time')
    except Exception:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
    start_time = TimeRep(time_element.text)
    channel = -1
    summary = 'dummy'
    return ProgramDescription(channel=channel, start_time=start_time, summary=summary)
    #return element


def get_program_table(html_element):
    program_list = filter(
        lambda x: x.get_attribute('id') == 'tvpgm',
        html_element.find_elements_by_tag_name('div')
        )

    try:
        program_frame = next(program_list)
    except StopIteration:
        raise AttributeError('No TV program is not available')

    tables = program_frame.find_elements_by_tag_name('table')
    assert len(tables) == 3

    return tables[-1]


def filter_cell(cell):
    print(cell.tag_name)
    return cell.tag_name == 'td'


def gen_programs(program_table):
    for cell in filter(filter_cell, program_table.find_elements_by_class_name('turnup')):
        program = cell.find_element_by_class_name('detail')
        yield element2description(program)

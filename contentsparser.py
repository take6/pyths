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

    def asstring(self):
        return self.__ts


ProgramDescription = collections.namedtuple(
    'ProgramDescription',
    ['channel', 'start_time', 'title', 'summary']
    )


def print_program(desc):
    print('{}ch {}~ {}'.format(desc.channel, desc.start_time, desc.title))


def get_start_time(element):
    try:
        time_element = element.find_element_by_class_name('time')
    except Exception:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
    start_time = TimeRep(time_element.text)
    return start_time


def get_channel(element):
    try:
        title_element = element.find_element_by_tag_name('a')
    except Exception:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
    data_ylk = title_element.get_attribute('data-ylk')
    channel = -1
    if data_ylk is not None:
        styles = data_ylk.split(';')
        gen_pos = filter(lambda x: x.strip().startswith('pos'), styles)
        try:
            pos = next(gen_pos)
            channel = int(pos.split(':')[1])
        except Exception as e:
            print('ERROR! {}'.format(str(e)))

    return channel


def get_title(element):
    try:
        title_element = element.find_element_by_tag_name('a')
    except Exception:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
    title = title_element.text
    return title


def element2description(element):
    start_time = get_start_time(element)
    channel = get_channel(element)
    title = get_title(element)
    summary = 'dummy'
    return ProgramDescription(channel=channel, start_time=start_time, title=title, summary=summary)


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
    _gen = filter(filter_cell, program_table.find_elements_by_class_name('turnup'))
    for cell in _gen:
        program = cell.find_element_by_class_name('detail')
        yield element2description(program)

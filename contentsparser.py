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
    ['station', 'start_time', 'title', 'summary']
    )


StationRep = collections.namedtuple(
    'StationRep',
    ['channel', 'name']
)


def str2StationRep(s):
    x = s.split('\n')
    assert len(x) == 2
    channel = int(x[0].strip('ch'))
    return StationRep(channel=channel, name=x[1])


def print_program(desc):
    print('{}ch {}~ {}'.format(desc.channel.channel, desc.start_time, desc.title))


def get_start_time(element):
    try:
        time_element = element.find_element_by_class_name('time')
    except Exception as e:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
        print(element.text)
        print(str(e))
    start_time = TimeRep(time_element.text)
    return start_time


def get_station(element, channel_map):
    try:
        title_element = element.find_element_by_tag_name('a')
    except Exception as e:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
        print(element.text)
        print(str(e))
    data_ylk = title_element.get_attribute('data-ylk')
    station = None
    if data_ylk is not None:
        styles = data_ylk.split(';')
        gen_pos = filter(lambda x: x.strip().startswith('pos'), styles)
        try:
            pos = next(gen_pos)
            channel_id = int(pos.split(':')[1])
            assert channel_id in channel_map
            station = channel_map[channel_id]
        except Exception as e:
            print('ERROR! {}'.format(str(e)))

    return station


def get_title(element):
    try:
        title_element = element.find_element_by_tag_name('a')
    except Exception as e:
        print('ERROR! <{} class="{}"'.format(element.tag_name, element.get_attribute('class')))
        print(element.text)
        print(str(e))
    title = title_element.text
    return title


def element2description(element, channel_map):
    # exclude non-program contents
    if element.text.find('番組のデータがありません') >= 0 or element.text.find('放送休止') >= 0:
        return None

    start_time = get_start_time(element)
    station = get_station(element, channel_map)

    # exclude programs earlier than 4am
    if start_time.asint() < 240:
        return None

    title = get_title(element)
    summary = 'dummy'
    return ProgramDescription(station=station, start_time=start_time, title=title, summary=summary)


def get_channel_map(html_element):
    stations = html_element.find_elements_by_class_name('station')
    assert len(stations) == 16
    num_stations = len(stations) // 2
    channel_map = dict(
        (i + 1, str2StationRep(s.text)) for i, s in enumerate(stations[:num_stations])
    )
    return channel_map


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
    return cell.tag_name == 'td'


def gen_program(program_table, channel_map):
    _gen = filter(filter_cell, program_table.find_elements_by_class_name('turnup'))
    for cell in _gen:
        program = cell.find_element_by_class_name('detail')
        desc = element2description(program, channel_map)
        if desc is not None:
            yield desc


def gen_program_record(html_element):
    channel_map = get_channel_map(html_element)
    program_table = get_program_table(html_element)
    return gen_program(program_table, channel_map)

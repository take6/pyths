import collections
import numpy

from .contentsparser import ProgramDescription
from .contentsparser import TimeRep
from . import util


def classify_by_channel(records):
    programs_by_channel = collections.defaultdict(list)
    for record in records:
        programs_by_channel[record.station].append(record)

    for station in programs_by_channel.keys():
        v = programs_by_channel[station]
        programs_by_channel[station] = add_duration(filter_by_time(v))

    return programs_by_channel


def filter_by_time(records):
    start_times = numpy.asarray(
        [record.start_time.asint() for record in records]
    )
    dt = start_times[1:] - start_times[:-1]
    i = numpy.where(dt < 0)[0]
    if len(i) == 0:
        return records
    else:
        return records[:i[0] + 1]


def set_duration(record, duration, next_day=False):
    stint = record.start_time.asint() % (24 * 60)
    if next_day:
        stint += 24 * 60
    start_time = TimeRep('{:02d}:{:02d}'.format(stint // 60, stint % 60))

    return ProgramDescription(
        station=record.station,
        start_time=start_time,
        duration=duration,
        title=record.title,
        summary=record.summary
    )


def add_duration(records):
    next_day = False

    for i in range(len(records) - 1):
        prog_now = records[i]
        prog_next = records[i + 1]
        start = prog_now.start_time.asint() % (24 * 60)
        end = prog_next.start_time.asint() % (24 * 60)
        # assert start <= end
        duration = end - start
        if duration < 0:
            duration += 24 * 60
            records[i] = set_duration(prog_now, duration, next_day=next_day)
            next_day = True
        else:
            records[i] = set_duration(prog_now, duration, next_day=next_day)

    # set dummy duration for the last record
    start = records[-1].start_time.asint()
    duration = 60 - start % 60
    if duration == 0:
        duration = 60
    records[-1] = set_duration(records[-1], duration, next_day=next_day)

    return records


def export(program_list, outfile=None, datestr=None):
    if datestr is None:
        datestr = util.str_tomorrow()

    if outfile is None:
        # default file name is "progYYYYMMDD.txt"
        outfile = 'prog{}.csv'.format(datestr)

    with open(outfile, 'w') as f:
        for station, programs in program_list.items():
            channel = station.channel
            for program in programs:
                start_time = program.start_time.asstring()
                duration = program.duration
                title = program.title
                summary = program.summary
                is_ths = 0  # default is False
                is_suspense = 0  # default is False
                row = '{}\n'.format(
                    ','.join(map(str, [datestr, channel, start_time, duration, title, summary, is_suspense, is_ths]))
                )
                f.write(row)

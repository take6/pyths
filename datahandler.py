import collections
import numpy

from .contentsparser import ProgramDescription
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


def set_duration(record, duration):
    return ProgramDescription(
        station=record.station,
        start_time=record.start_time,
        duration=duration,
        title=record.title,
        summary=record.summary
    )


def add_duration(records):
    for i in range(len(records) - 2):
        prog_now = records[i]
        prog_next = records[i + 1]
        start = prog_now.start_time.asint()
        end = prog_next.start_time.asint()
        assert start <= end
        duration = end - start
        records[i] = set_duration(prog_now, duration)

    # set dummy duration for the last record
    start = records[-1].start_time.asint()
    duration = start % 60
    if duration == 0:
        duration = 60
    records[-1] = set_duration(records[-1], duration)

    return records


def export(program_list, outfile=None):
    if outfile is None:
        # default file name is "progYYYYMMDD.txt"
        outfile = 'prog{}.txt'.format(util.str_tomorrow())

    with open(outfile, 'w') as f:
        f.write('こんにちは！\n')
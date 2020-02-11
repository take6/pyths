import collections
import numpy


def classify_by_channel(records):
    programs_by_channel = collections.defaultdict(list)
    for record in records:
        programs_by_channel[record.station].append(record)

    for station in programs_by_channel.keys():
        v = programs_by_channel[station]
        programs_by_channel[station] = filter_by_time(v)

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


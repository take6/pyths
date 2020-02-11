import collections


def classify_by_channel(records):
    programs_by_channel = collections.defaultdict(list)
    for record in records:
        programs_by_channel[record.station.channel].append(record)

    return programs_by_channel


def sort_by_time(records):
    pass
import selenium


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


def get_program_list(program_table):
    pass
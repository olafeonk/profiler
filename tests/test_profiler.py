import os

from modules.Core import ProfilerCore

PATH = os.path.dirname(__file__)


def test_simple_program():
    globs = {'__file__': 'hello.py', '__name__': '__main__',
             '__package__': None, '__cached__': None, }
    result_1 = {'sleep_for_2_sec': 3, 'sleep_for_4_sec': 1, 'main': 1,
                'new_func': 2, '<module>': 1}

    core = ProfilerCore(globs, [], PATH, 'time', 10)
    core.start()

    statistics = core.calculated_stat
    for func in statistics.keys():
        assert result_1[func] == statistics[func].n_calls


def test_program_with_args():
    args = [36, 23, 571, 74654]
    globs = {'__file__': 'calculator.py', '__name__': '__main__',
             '__package__': None, '__cached__': None}
    core = ProfilerCore(globs, args, PATH, 'time', 1)
    core.start()

    statistics = core.calculated_stat
    assert 10 == len(statistics)

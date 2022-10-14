import os

from modules.OuputFormatter import OutputFormatter
from modules.Profiler import Profiler
from modules.StatisticCalculator import StatisticCalculater


class ProfilerCore:
    def __init__(self, globs, argv, workdir, sort_by, interval) -> None:
        self.globs = globs
        self.argv = argv
        self.workdir = workdir
        self.sort_by = sort_by
        self.interval = interval
        self.prog_name = globs['__file__']
        self.stat_calculater = StatisticCalculater()
        self.calculated_stat = None

        self.globs['__file__'] = os.path.join(self.workdir, self.prog_name)

    def start(self) -> None:
        profiler = Profiler(self.globs, self.argv, self.interval)
        profiler.start()
        self.stat_calculater.update_raw_data(profiler.raw_data)
        self.calculated_stat = self.stat_calculater.calc_statistics()
        o = OutputFormatter(self.prog_name, self.sort_by)
        o.intro()
        o.create_output(self.calculated_stat)

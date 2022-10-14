class OutputFormatter:
    def __init__(self, filename, sort_by) -> None:
        self.filename = filename
        self.sort_by = sort_by

    def intro(self) -> None:
        print(f'  Ordered by: {self.sort_by}')
        header = ['ncalls', 'tottime', 'percall', 'cumtime', 'percall',
                  'maxtime', 'mintime', 'medtime', 'filename:(function)']

        for column in header:
            print(f"{column: >8}", end=" ")
        print()

    def create_output(self, stats) -> None:
        sorted_output = self._sort_output(stats)
        for key, value in sorted_output.items():
            n_calls = value.n_calls
            total_time = value.total_time
            per_call1 = value.per_call1
            per_call2 = value.per_call2
            cumtime = value.cumtime
            max_time = value.max_time
            min_time = value.min_time
            med_time = value.med_time
            print(f"{n_calls: >8}"
                  f" {total_time: >8}"
                  f" {per_call2: >8}"
                  f" {cumtime: >8}"
                  f" {per_call1: >8}"
                  f" {max_time: >8}"
                  f" {min_time: >8}"
                  f" {med_time: >8}"
                  f" {self.filename}:({key})", end="\n"
                  )

    def _sort_output(self, stats) -> dict:
        if self.sort_by == 'time':
            return dict(sorted(stats.items(), key=lambda item: item[1].cumtime,
                               reverse=True))
        if self.sort_by == 'calls':
            return dict(sorted(stats.items(), key=lambda item: item[1].n_calls,
                               reverse=True))
        if self.sort_by == 'percall':
            return dict(sorted(stats.items(), key=lambda item: item[1].percall,
                               reverse=True))
        return stats

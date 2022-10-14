import statistics


class ProgStatistics:
    def __init__(self):
        self.funcs = {}

    def update_statistics(self, func) -> None:
        step_number = func[0]
        f_name = func[3]
        f_called_order = func[4]
        f_time_step = func[5]
        f_args = func[6]
        self._update(f_name, step_number, f_called_order, f_time_step, f_args)
        self._cum_update(step_number, f_called_order, f_time_step)

    def _cum_update(self, step_number, called_order, time_step) -> None:
        for i in range(len(called_order) - 1, -1, -1):
            call = called_order[i]
            f_name, f_lineno = call[0], call[1]
            try:
                self.funcs[f_name].cumtime += time_step
            except KeyError:
                self.funcs[f_name] = FuncStatistics(step_number, [], [])
                self.funcs[f_name].cumtime += time_step

    def final_calc(self) -> None:
        for value in self.funcs.values():
            value.sub_calc()
            for f_name in value.was_called_from:
                self.funcs[f_name].total_time -= value.cumtime
        for value in self.funcs.values():
            value.final_calc()

    def _update(self, name, step_number, called_order, time_step, args) -> None:
        try:
            self.funcs[name].update_statistics(step_number, called_order,
                                               time_step, args)
        except KeyError:
            self.funcs[name] = FuncStatistics(step_number, called_order, args)
            self.funcs[name].update_statistics(step_number, called_order,
                                               time_step, args)


class FuncStatistics:
    def __init__(self, step_number, called_order, args) -> None:
        self.last_step = step_number
        self.n_calls = 1
        self.total_time = 0
        self.per_call1 = 0
        self.per_call2 = 0
        self.cumtime = 0
        self.max_time = 0
        self.min_time = 0
        self.med_time = 0
        self.called_order = called_order
        self.was_called_from = set()
        self.current_period = 0
        self.args = args
        self.worked_times = []

    def update_statistics(self, step_number, called_order, time_step, args) -> None:

        same_call = self._check_same_conditions(step_number, called_order, args)

        if same_call:
            self.current_period += time_step
            self.last_step = step_number

        else:
            self.n_calls += 1
            if self.current_period > 0:
                self.worked_times.append(self.current_period)

            for func in self.called_order:
                self.was_called_from.add(func[0])
            self.called_order = called_order
            self.args = args
            self.current_period = 0
            self.last_step = step_number

    def _check_same_conditions(self, step_number, called_order, args) -> bool:
        if step_number - self.last_step > 1:
            return False
        if len(self.called_order) != len(called_order):
            return False
        for i in range(len(called_order)):
            for j in range(2):
                if self.called_order[i][j] != called_order[i][j]:
                    return False

        if len(self.args) != len(args):
            return False
        for key, value in args.items():
            try:
                result = self.args[key]
            except KeyError:
                return False
            if result != value:
                return False
        return True

    def sub_calc(self) -> None:
        if self.current_period > 0:
            self.worked_times.append(self.current_period)
            for func in self.called_order:
                self.was_called_from.add(func[0])
        self.cumtime = round(self.cumtime + sum(self.worked_times), 2)

    def final_calc(self) -> None:
        self.total_time = round(self.total_time + self.cumtime, 2)
        if self.total_time < 0:
            self.total_time = 0
        else:
            self.total_time = round(self.total_time, 2)
        self.per_call1 = round(self.cumtime / self.n_calls, 2)
        self.per_call2 = round(self.total_time / self.n_calls, 2)
        if len(self.worked_times) > 0:
            self.max_time = round(max(self.worked_times), 3)
            self.min_time = round(min(self.worked_times), 3)
            self.med_time = round(statistics.median(self.worked_times), 3)

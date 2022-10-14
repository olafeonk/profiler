import os
import sys
import threading
import time
import traceback

FILENAME = os.path.abspath(__file__)


def worker(code, globs, args) -> None:
    try:
        sys.argv = args
        exec(code, globs)
    except Exception as e:
        print(e)
        raise


class Profiler:
    def __init__(self, globs, args, interval) -> None:
        self.globs = globs
        self.interval = 1 / 1000 * interval

        with open(globs['__file__'], 'rb') as fp:
            self.code = compile(fp.read(), globs['__file__'], 'exec')

        self.args = [globs['__file__']]
        if args is not None:
            for a in args:
                self.args.append(a)

        self.profile_object = threading.Thread(target=worker,
                                               args=[self.code, self.globs,
                                                     self.args], daemon=True)
        self.stack_screens = []
        self.raw_data = []
        self.worked_time = 0

    def start(self) -> None:
        self.worked_time = time.time()
        self.profile_object.start()
        profiling_thread_id = self.profile_object.ident

        try:
            self._main_loop(profiling_thread_id)
        except KeyboardInterrupt:
            self.worked_time = time.time() - self.worked_time
            self.raw_data = self._prettify_stack_screens()
            return
        self.worked_time = time.time() - self.worked_time
        self.raw_data = self._prettify_stack_screens()

    def _main_loop(self, profiling_thread_id) -> None:
        stack_search_time = 0

        while self.profile_object.is_alive():
            if self.interval - stack_search_time > 0:
                time.sleep(self.interval - stack_search_time)

            time_start = time.time()

            for thread_id, stack in sys._current_frames().items():
                if thread_id == profiling_thread_id:
                    call_stack = []
                    args = stack.f_locals
                    for frame in traceback.extract_stack(stack):
                        filename = frame[0]
                        if filename == self.globs['__file__']:
                            call_stack.append(frame)
                    if call_stack:
                        self.stack_screens.append((call_stack, args))

            stack_search_time = time.time() - time_start

    def _prettify_stack_screens(self) -> list:
        result = []
        time_per_screen = self.worked_time / len(self.stack_screens)
        time_step = 1
        for stack, args in self.stack_screens:
            called_before = []
            func = stack[len(stack) - 1]
            for i in range(len(stack) - 1):
                frame = stack[i]
                called_before.append((frame.name, frame.lineno))
            f_name = os.path.basename(func.filename)
            result.append((time_step, f_name, func.lineno, func.name,
                           called_before, time_per_screen, args))
            time_step += 1
        return result

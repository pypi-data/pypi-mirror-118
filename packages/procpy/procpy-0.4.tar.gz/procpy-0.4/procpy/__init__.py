#  MIT License
#
#  Copyright (c) 2021 Pascal Eberlein
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from multiprocessing import Process as Proc
from multiprocessing import Queue
from time import sleep


class Process(Proc):
    _do_run: bool = False

    def __init__(self, **kwargs):
        Proc.__init__(self)
        self.__dict__.update(kwargs)
        self._do_run = True

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def work(self):
        raise Exception("Overwrite me")

    def run(self) -> None:
        self.on_start()
        while self._do_run:
            self.work()
        self.on_stop()

    def stop(self):
        self._do_run = False

    def sleep(self, n: float):
        try:
            sleep(n)
        except KeyboardInterrupt:
            self.stop()
            pass

    def is_running(self):
        return self._do_run


__all__ = ["Process", "Queue"]

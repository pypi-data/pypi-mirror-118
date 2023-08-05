# -*- coding: utf-8 -*-

import logsloth


# class LogSlothTest(unittest.TestCase):
class LogSlothTest:
    @logsloth.fun_scope
    def test_basic(self):
        logsloth.d("hello")
        logsloth.caller("cmd123")

        for _ in range(5):
            logsloth.d("work ...")

        logsloth.callee("cmd123")
        logsloth.d("world")
        # self.assertTrue(True)


if __name__ == '__main__':
    logsloth.init(show_color=False)
    # unittest.main()
    LogSlothTest().test_basic()

import os


class TemporaryDir:
    __directories_stack = []

    @staticmethod
    def enter(dir_name):
        TemporaryDir.__directories_stack.append(os.getcwd())
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.chdir(dir_name)

    @staticmethod
    def leave():
        if len(TemporaryDir.__directories_stack) > 0:
            os.chdir(TemporaryDir.__directories_stack.pop())


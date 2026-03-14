from .ArgumentBuilder import ArgumentBuilder

class Command:
    def __init__(self, executable: str):
        self.executable = executable
        self.builder = ArgumentBuilder()

    def add_args(self, *args):
        for arg in args:
            self.builder._args.append(arg)
        return self

    @property
    def args(self):
        return self.builder.build()
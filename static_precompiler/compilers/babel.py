import os.path

from static_precompiler import exceptions, utils

from . import base

__all__ = (
    "Babel",
)


class Babel(base.BaseCompiler):

    name = "babel"
    input_extension = "es6"
    output_extension = "js"

    def __init__(self, executable="babel", modules=None):
        self.executable = executable
        self.modules = modules
        super(Babel, self).__init__()

    def compile_file(self, source_path):
        return self.compile_source(self.get_source(source_path))

    def compile_source(self, source):
        args = [
            self.executable
        ]

        if self.modules is not None:
            args.extend(["--modules", self.modules])

        out, errors = utils.run_command(args, source)
        if errors:
            raise exceptions.StaticCompilationError(errors)

        return out

    def compile_source_to_file(self, source_path):
        source = self.get_source(source_path)
        output_path = self.get_full_output_path(source_path)
        output_dir = os.path.dirname(output_path)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        args = [
            self.executable,
            '--source-maps', 'true',
            '--out-file', output_path,
            self.get_full_source_path(source_path)
        ]

        if self.modules is not None:
            args.extend(["--modules", self.modules])

        out, errors = utils.run_command(args)
        if errors:
            raise exceptions.StaticCompilationError(errors)
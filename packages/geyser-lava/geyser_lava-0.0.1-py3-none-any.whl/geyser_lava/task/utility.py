from datetime import datetime
from logging import Logger
from os import makedirs, environ
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Text
from uuid import uuid4

from geyser import Geyser, Task


@Geyser.task(provides=('path',))
class PathProvider(Task):
    class Provider(object):
        _tempdir = TemporaryDirectory(suffix='_folder', prefix='geyser_')
        _homedir = Path.home().absolute()
        _curdir = Path('geyser').absolute()

        @classmethod
        def _makedirs_join(cls, *args, root_dir) -> Path:
            new_path = root_dir.joinpath(*args)
            try:
                makedirs(new_path.parent)
            except FileExistsError:
                pass
            return new_path

        def temporary(self, *args) -> Path:
            root_dir = Path(self._tempdir.name).absolute()
            return self._makedirs_join(*args, root_dir=root_dir)

        def home(self, *args) -> Path:
            root_dir = self._homedir.joinpath('geyser')
            return self._makedirs_join(*args, root_dir=root_dir)

        def current(self, *args) -> Path:
            root_dir = self._curdir / 'geyser'
            return self._makedirs_join(*args, root_dir=root_dir)

    def execute(self, *args, **kwargs):
        return self.Provider(),


@Geyser.task(provides=('env',))
class EnvProvider(Task):
    def execute(self, *args, logger: Logger, **kwargs):
        for key, value in self.inject.items():
            if key != 'logger':
                logger.debug(f'Inject {key}={value} into environment value')
                environ[key] = value

        return environ,


@Geyser.task(provides=('id',))
class IdProvider(Task):
    def execute(self, *args, title: Text = None, **kwargs):
        uuid = uuid4().hex
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if title is None:
            return f'{timestamp}_{uuid}',
        else:
            return f'{title}_{timestamp}_{uuid}',

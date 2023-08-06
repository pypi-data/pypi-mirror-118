import os
import re
import yaml

from .colors import colors
from .files import FilePlan
from .run import run


async def parse(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = await parse(value)

    elif isinstance(data, list):
        data = [await parse(value) for value in data]

    elif isinstance(data, str):
        for var in re.findall(r'\${[^}]+}', data):
            if ':' in var:
                name, default = var[2:-1].split(':')
            elif '-' in var:
                name, default = var[2:-1].split('-')
            else:
                name = var[2:-1]
                default = ''
            if name in os.environ:
                data = data.replace(var, os.environ[name])
            else:
                data = data.replace(var, default)

        for sub in re.findall(r'\$\([^)]+\)', data):
            rc, out, err = await run('sh', '-c', sub[2:-1], verbose=False)
            data = data.replace(sub, out.decode('utf8').strip())

    return data


class ComposeConfig:
    @classmethod
    def factory(cls, method, root, config, name, *filters):
        for path, data in config[name].items():
            yield ComposePlan(root, config, path, **data)


class ComposePlan(FilePlan):
    async def content(self):
        return yaml.dump(await parse(dict(self)))

    async def activate(self):
        path = self.path()
        if not path.exists():
            return

        dirname = os.path.dirname(path)
        cwd = os.getcwd()
        try:
            os.chdir(dirname)
            for cmd in ('up --detach', 'logs', 'ps'):
                await run(f'docker-compose -f {path} {cmd}')
        finally:
            os.chdir(cwd)

        print(''.join([
            colors['greenbold'],
            '✔ ',
            colors['reset'],
            colors.color(251),
            'Started ',
            str(self.name),
            colors['reset'],
        ]))

    async def destroy(self):
        path = self.path()
        if not path.exists():
            return

        cwd = os.getcwd()
        try:
            os.chdir(os.path.dirname(path))
            await run(f'docker-compose -f {path} down --volumes')
        finally:
            os.chdir(cwd)

        path.unlink()

        return ''.join([
            colors['greenbold'],
            '✔ ',
            colors['reset'],
            colors.color(251),
            'Destroyed ',
            str(self.name),
            colors['reset'],
        ])

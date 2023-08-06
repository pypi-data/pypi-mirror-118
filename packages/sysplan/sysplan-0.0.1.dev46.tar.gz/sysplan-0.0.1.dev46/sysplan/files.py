from pathlib import Path
import os

from .colors import colors
from .plan import Plan
from .diff import difftext
from .run import run


class FilePlan(Plan):
    def path(self):
        return Path(os.path.join(self.root, self.name.lstrip('/')))

    async def content(self):
        return self['content']

    async def diff(self):
        self.path = self.path()
        if os.path.exists(self.path):
            current_file = self.path
            with open(self.path, 'r') as f:
                current_content = f.read()
        else:
            current_file = '/dev/null'
            current_content = ''
        content = await self.content()
        return difftext(
            from_file=current_file,
            to_file=self.path,
            to_content=content.split('\n'),
            from_content=current_content.split('\n'),
        )

    async def write(self):
        diff = await self.diff()
        if diff:
            dirname = os.path.dirname(self.path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(self.path, 'w') as f:
                f.write(await self.content())

        if 'mode' in self:
            await run(f'chmod {self["mode"]} {self.path}')

        if 'owner' in self:
            await run(f'chown {self["owner"]} {self.path}')

        if 'group' in self:
            await run(f'chgrp {self["group"]} {self.path}')

        print(''.join([
            colors['greenbold'],
            '✔ ',
            colors['reset'],
            colors.color(251),
            'Wrote ',
            str(self.path),
            colors['reset'],
        ]))
        return diff

    async def destroy(self):
        path = self.path()
        if path.exists():
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

import os
from functools import cached_property

from utils import WWW, File, JSONFile, Log

from lkas import extract
from openaix.Humanizer import Humanizer

log = Log('LKActSimple')


class LKActSimple:
    def __init__(self, id: str):
        self.id = id

    @property
    def url(self) -> str:
        return '/'.join(
            [
                'https://raw.githubusercontent.com/nuuuwan/lk_acts',
                'main/data',
                id,
                'data.json',
            ]
        )

    @cached_property
    def data(self):
        data_path = WWW(self.url).download()
        return JSONFile(data_path).read()

    @property
    def preamble(self):
        return '\n'.join(self.data['preamble_lines'])

    @property
    def parts(self):
        return [extract.part(x) for x in self.data['parts']]

    @property
    def humanized_lines(self):
        lines = [
            '# Preamble',
            Humanizer.translate([self.preamble]),
        ]
        for i, part in enumerate(self.parts[:2]):
            lines.append(f'# Part {i+1}')
            lines.append(Humanizer.translate([part]))

        return lines

    def write(self):
        content = '\n\n'.join(self.humanized_lines)
        path = os.path.join('data', f'{self.id}.md')
        File(path).write(content)
        log.debug(f'Wrote {path}')


if __name__ == '__main__':
    id = '2022-0099-personal-data-protection'
    LKActSimple(id).write()

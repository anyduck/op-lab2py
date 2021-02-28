#!/usr/bin/python
from pathlib import Path
from collections import namedtuple


InputLine = namedtuple('InputLine', ['surname', 'r1', 'r2', 'r3', 'r4', 'r5', 'is_contractor'])
OutputLine = namedtuple('OutputLine', ['surname', 'rating'])


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']

def csv2list(path: Path) -> list[InputLine]:
    result = []
    with open(path, 'r') as csv:
        for line in csv.readlines()[1:]: # Пропускаємо перший рядок
            result.append(InputLine(*line.split(',')))
    return result


def main(folder: Path, output: Path) -> None:
    files = find_csv(folder)
    print(csv2list(files[0]))


if __name__ == '__main__':
    folder = Path(input('Введіть теку з фалами: '))
    main(folder, output=Path('rating.csv'))

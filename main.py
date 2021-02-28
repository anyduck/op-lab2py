#!/usr/bin/python
from pathlib import Path
from collections import namedtuple


InputLine = namedtuple('InputLine', ['surname', 'rating', 'is_contractor'])
OutputLine = namedtuple('OutputLine', ['surname', 'rating_avg'])


def list2input_line(line: list) -> InputLine:
    """ Конвертує список вхідних даних в InputLine. """

    def flag2bool(flag: str) -> bool:
        """ Перетворює текстовий флаг в булеву змінну. """

        if flag.lower() in ('true', 'yes'):
            return True
        if flag.lower() in ('false', 'no'):
            return False
        raise ValueError(f'Невідомий флаг {flag}')

    surname: str = line[0]
    rating: tuple = tuple(int(r) for r in line[1:5])
    is_contractor: bool = flag2bool(line[6])

    return InputLine(surname, rating, is_contractor)


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']


def csv2list(path: Path) -> list[InputLine]:
    """ Конвертує вміст csv в список InputLine-ів. """

    result = []
    with open(path, 'r') as csv:
        for line in csv.readlines()[1:]:  # Пропускаємо перший рядок
            result.append(list2input_line(line.rstrip('\n').split(',')))
    return result


def main(folder: Path, output: Path) -> None:
    files = find_csv(folder)
    print(csv2list(files[0]))


if __name__ == '__main__':
    folder = Path(input('Введіть теку з фалами: '))
    main(folder, output=Path('rating.csv'))

#!/usr/bin/python
from pathlib import Path


def find_csv(folder: Path) -> list[Path]:
    """ Повертає список всіх *.csv файлів в теці. """

    return [path for path in folder.iterdir()
            if path.is_file() and path.suffix == '.csv']

def main(folder: Path, output: Path) -> None:
    print(find_csv(folder))


if __name__ == '__main__':
    folder = Path(input('Введіть теку з фалами: '))
    main(folder, output=Path('rating.csv'))

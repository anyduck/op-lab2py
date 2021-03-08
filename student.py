class Student:
    """ Студент. """

    def __init__(self, surname: str, rating: list[int], is_contractor: bool):
        self.surname: str = surname
        self.rating: list[int] = rating
        self.is_contractor: bool = is_contractor

    @property
    def rating_avg(self) -> float:
        """ Повертає середній рейтинг студента. """

        return round(sum(self.rating) / len(self.rating), 3)

    def to_rating_list(self) -> list[str]:
        """ Створює список з прізвищем і середнім рейтингом. """

        return [self.surname, str(self.rating_avg)]

    @classmethod
    def from_list(cls, student: list[str]):
        """ Створює зі списку параметрів. """

        surname: str = student[0]
        rating: list = [int(r) for r in student[1:6]]
        is_contractor: bool = _flag2bool(student[6])

        return cls(surname, rating, is_contractor)


def _flag2bool(flag: str) -> bool:
    """ Перетворює текстовий флаг в булеву змінну. """

    if flag.lower() in ('true', 'yes'):
        return True
    if flag.lower() in ('false', 'no'):
        return False
    raise ValueError(f'Невідомий флаг {flag}')

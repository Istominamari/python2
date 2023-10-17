#Треугольник существует только тогда, когда сумма любых двух его сторон
# больше третьей. Дано a, b, c - стороны предполагаемого треугольника. 
# Требуется сравнить длину каждого отрезка-стороны с суммой двух других. 
# Если хотя бы в одном случае отрезок окажется больше суммы двух других, 
# то треугольника с такими сторонами не существует. Отдельно сообщить 
# является ли треугольник разносторонним, равнобедренным или равносторонним.

import logging
import argparse

logging.basicConfig(filename='triangle.log',
                    encoding='UTF-8',
                    format='{levelname:<8} - {asctime}. {funcName}()::{lineno}: {msg}',
                    style='{',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

class SideError(Exception):
    def __init__(self, value):
        self.message = f'Отрицательная грань ({value}) не может существовать.'
        super().__init__(self.message)

class TriangleError(Exception):
    def __init__(self, a, b, c):
        self.message = f'Треугольник с такими гранями ({a}, {b}, {c}) не может существовать.'
        super().__init__(self.message)

def decor(func):
    def wrapper(*args, **kwargs):
        logger.info(f'Вызвана функция {func.__name__} c аргументами {args}.')
        try:
            result = func(*args, **kwargs)
        except SideError as e:
            logger.fatal(e.message)
            return e.message
        except TriangleError as e:
            logger.error(e.message)
            return e.message
        logger.info(f'Выполнена функция {func.__name__} с результатом "{result}".')
        return result
    return wrapper

@decor
def triangle_type(a, b, c):
    if a < 0:
        raise SideError(a)
    if b < 0:
        raise SideError(b)
    if c < 0:
        raise SideError(c)

    if a == 0 or b == 0 or c == 0:
        logger.warning('Указана нулевая грань.')

    if a + b <= c or a + c <= b or b + c <= a:
        raise TriangleError(a, b, c)

    logger.debug(f'Периметр: {a + b + c}')

    if a != b and b != c and a != c:
        return "Треугольник разносторонний"
    elif a == b and b == c:
        return "Треугольник равносторонний"
    else:
        return "Треугольник равнобедренный"

parser = argparse.ArgumentParser(description="Определяет тип треугольника по размеру его граней")
parser.add_argument('-a', type=int, help="Размер первой грани", required=True)
parser.add_argument('-b', type=int, help="Размер второй грани", required=True)
parser.add_argument('-c', type=int, help="Размер третьей грани", required=True)
args = parser.parse_args()

print(triangle_type(args.a, args.b, args.c))
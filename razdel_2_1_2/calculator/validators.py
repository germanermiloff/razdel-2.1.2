from django.core.exceptions import ValidationError


def validate_inn(value):

    def check_inn(inn):
        if len(inn) == 10:
            coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
            control_number = sum(int(inn[i]) * coefficients[i] for i in range(10)) % 11 % 10
            return control_number == int(inn[-1])
        elif len(inn) == 12:
            coefficients1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
            control_number1 = sum(int(inn[i]) * coefficients1[i] for i in range(11)) % 11 % 10
            coefficients2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
            control_number2 = sum(int(inn[i]) * coefficients2[i] for i in range(12)) % 11 % 10
            return control_number1 == int(inn[-2]) and control_number2 == int(inn[-1])
        else:
            return False

    if not (len(value) == 10 or len(value) == 12) or not value.isdigit():
        raise ValidationError('ИНН должен содержать 10 или 12 цифр.')

    if not check_inn(value):
        raise ValidationError('Некорректный ИНН.')

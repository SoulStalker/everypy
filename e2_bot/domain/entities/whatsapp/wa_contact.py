import re


class WhatsAppContact:
    def __init__(self, phone_number, first_name, last_name="", email="", telegram_id=""):
        self._phone_number = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._telegram_id = None

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telegram_id = telegram_id

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not re.fullmatch(r'7\d{10}', value):
            raise ValueError("Номер телефона должен быть в формате 71234567890.")
        self._phone_number = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value.isalpha():
            raise ValueError("Имя должно содержать только буквы.")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is not None and not value.isalpha():
            raise ValueError("Фамилия должна содержать только буквы.")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is not None:
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.fullmatch(email_regex, value):
                raise ValueError("Некорректный формат email.")
        self._email = value

    @property
    def telegram_id(self):
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, value):
        self._telegram_id = value

    def __str__(self):
        return (f"Телефон: {self.phone_number}\n"
                f"Имя: {self.first_name}\n"
                f"Фамилия: {self.last_name}\n"
                f"Email: {self.email}\n"
                f"Телеграмм: {self.telegram_id}\n")

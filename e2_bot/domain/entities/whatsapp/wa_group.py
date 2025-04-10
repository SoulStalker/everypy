import re


class WhatsAppGroup:
    def __init__(self, group_id, group_name):
        self._group_id = None
        self._group_name = None

        self.group_id = group_id
        self.group_name = group_name

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        # Проверка, что group_id соответствует формату 18 цифр + @g.us
        if not re.fullmatch(r'^\d+@g\.us$', value):
            print(repr(value))
            raise ValueError("ID группы должен быть в формате любого количества цифр, за которыми следует '@g.us'.")
        self._group_id = value

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        # Проверка, что имя группы содержит только допустимые символы
        if not re.fullmatch(r'[\w\s\-\@\.\,]+', value):
            raise ValueError("Имя группы может содержать буквы, цифры, пробелы и следующие символы: - @ . ,")
        self._group_name = value

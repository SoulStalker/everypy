from e2_bot.domain.value_objects import Command

LEXICON_COMMANDS: dict[str, str] = {
    Command.START.value: 'Запуск бота',
    Command.HELP.value: 'Справка по работе бота',
    Command.SETTINGS.value: 'Настройка',
    Command.CONTACTS.value: 'Контакты',
    Command.UNCLOSED.value: 'Незакрытые смены'
}

LEXICON: dict[str, str] = {
    '/start': 'Привет! 👋\nЯ бот помощник для сисадминов\n'
              'Все команды в разделе /help 🆘\n',
    '/help': '/unclosed - список незакрытых смен\n/service можно провести дополнительные настройки бота\n',
    '/service': '⚙️ Тут можно будет что-то настроить\n',
    '/contacts': 'По вопросом можно связаться через аккаунт @SoulStalk3r\n',
}

from e2_bot.domain.value_objects import UserCommand

LEXICON_COMMANDS: dict[str, str] = {
    UserCommand.START.value: 'Запуск бота',
    UserCommand.HELP.value: 'Справка по работе бота',
    # UserCommand.SERVICE.value: 'Настройка',
    # UserCommand.CONTACTS.value: 'Контакты',
    UserCommand.UNCLOSED.value: 'Незакрытые смены',
    UserCommand.TOTAL.value: 'Итоги за день',
    UserCommand.RESULTS_BY_SHOP.value: 'Результаты по магазинам',
    UserCommand.OTRS_STATS.value: 'Статистика OTRS',
    UserCommand.EQUIPMENT.value: 'Оборудование на складе',
}

LEXICON: dict[str, str] = {
    '/start': 'Привет! 👋\nЯ бот помощник для сисадминов\n'
              'Все команды в разделе /help 🆘\n',
    '/help': '/unclosed - список незакрытых смен\n/total - Итоги за день\n/otrs_stats - Статистика OTRS\n/equipment - Оборудование на складе\n',
    '/service': '⚙️ Тут можно будет что-то настроить\n',
    '/contacts': 'По вопросом можно связаться через аккаунт @SoulStalk3r\n',
}

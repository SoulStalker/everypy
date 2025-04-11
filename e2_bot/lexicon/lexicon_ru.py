from e2_bot.domain.value_objects import UserCommand

LEXICON_COMMANDS: dict[str, str] = {
    UserCommand.START.value: 'Запуск бота',
    UserCommand.HELP.value: 'Справка по работе бота',
    UserCommand.SERVICE.value: 'Настройка',
    UserCommand.CONTACTS.value: 'Контакты',
    UserCommand.UNCLOSED.value: 'Незакрытые смены',
    UserCommand.TOTAL.value: 'Итоги за день',
    UserCommand.RESULTS_BY_SHOP.value: 'Результаты по магазинам',
    UserCommand.OTRS_STATS.value: 'Статистика OTRS',
    UserCommand.EQUIPMENT.value: 'Оборудование на складе',
}

LEXICON: dict[str, str] = {
    '/start': '👋 Привет!\nЯ — бот-помощник для сисадминов 💻\nВсе доступные команды — в разделе /help 🆘',

    '/help': '🛠 <b>Доступные команды:</b>\n\n'
             '📂 <b>/unclosed</b> — список незакрытых смен\n'
             '📊 <b>/total</b> — итоги за день\n'
             '📈 <b>/otrs_stats</b> — статистика OTRS\n'
             '🏷 <b>/equipment</b> — оборудование на складе',

    '/service': '⚙️ Здесь в будущем появятся настройки бота\n',

    '/contacts': '📞 <b>Контакты:</b>\nПо вопросам пиши @SoulStalk3r',

    'get_groups': '📋 Группы',
    'get_contacts': '👥 Контакты',

    'add_group': '➕ Добавить новую группу',
    'add_contact': '➕ Добавить новый контакт',

    'delete_group': '🗑 Удалить группу',
    'delete_contact': '🗑 Удалить контакт',

    'cancel': '❌ Отмена',
    'choose_action': '🤖 Выбери действие из списка:',

    'input_phone': '📱 Введи номер телефона в формате <code>79999999999</code>:',
    'input_contact_name': '👤 Введи <b>имя</b> контакта:',
    'input_contact_last_name': '👤 Введи <b>фамилию</b> контакта:',
    'input_contact_email': '📧 Введи <b>email</b> контакта:',
    'input_contact_tg': '💬 Введи <b>Telegram ID</b> контакта:',

    'input_group_name': '🏷 Введи <b>название группы</b>:',
    'input_group_id': '🆔 Введи <b>ID группы</b>:',

    'contact_exist': '⚠️ Такой контакт уже существует!',
    'group_exist': '⚠️ Такая группа уже существует!',
}



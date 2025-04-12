import datetime
import calendar
import random

from loguru import logger
from otrs_service.app.db import DataAnalyzer, session_maker
from otrs_service.app.constants import TgAnswer


async def get_message(analyzer, period):
    """
    Возвращает сообщение для телеги со смайликами
    :param analyzer:
    :param period:
    :return:
    """
    strongs = []
    poos = {}

    strong = '   \U0001F4AA\n'
    good = '   \U0001F44D\n'
    little = '   \U0001F90F\n'
    poo = '   \U0001F4A9\n'
    if period == 'сегодня':
        multiplier = 1
        await analyzer.get_results()
    elif period == 'месяц':
        multiplier = 10
        await analyzer.get_month_results()
    message = f'За {period} закрыли заявки: \n\n'
    for result in analyzer.results:
        agent = f' - {result[0]} {result[1]} - '
        tickets = result[2]
        message += agent
        message += str(tickets)
        if tickets >= 15 * multiplier:
            message += strong
            strongs.append(result[0])
        elif tickets >= 10 * multiplier:
            message += good
        elif tickets >= 5 * multiplier:
            message += little
        else:
            message += poo
            poos.setdefault(result[0], result[2])
    if len(poos) > 0:
        hero = min(poos.items(), key=lambda x: x[1])
        # end_word = bad_work(hero[0])
        end_word = TgAnswer.BAD_BOY.value
    else:
        # end_word = 'Надо же как отработали, ни одной какахи'
        end_word = TgAnswer.GOOD_BOY.value
    if len(strongs) > 0:
        # super_hero = max(strongs, key=lambda x: x[1])
        # end_word = well_done(super_hero)
        end_word = TgAnswer.GOOD_BOY.value
    return message, end_word


def well_done(username):
    mess = [
        f"Спасибо, {username}, за то, что не дает нашим компьютерам помереть молча.",
        f"Наша поддержка похожа на чашку кофе - она всегда рядом и делает день лучше. Благодарим {username}!",
        f"{username} - как ниндзя в мире технической поддержки. Проблемы просто исчезают, когда он в деле!",
        f"С нашим {username} нет страха перед магическими словами '404' и 'ошибка сервера'!",
        f"{username} не нужны красные мантии - его костюм техподдержки смотрится лучше!",
        f"{username} наше решение для всех технических головоломок. На что бы мы делали без него?",
        f"Кто-то позвонил красной кнопке? А нет, это просто {username}, приходящий на помощь!",
        f"Похоже, {username} узнал секреты магии IT и щелкает пальцами, чтобы все работало!",
        f"{username} — наш цифровой супергерой. Даже Капитан Америка завидует его щиту от багов!",
        f"Спасибо, {username}, за то, что превращаешь наши ‘ошибки’ в ‘особенности работы’!",
        f"{username} — единственный, кто понимает, что ‘перезагрузка’ — это не просто совет, а образ жизни!",
        f"Если бы интернет был темным лесом, {username} был бы нашим GPS с вечным зарядом!",
        f"{username} не просто чинит сервера — он воскрешает их, как IT-некромант!",
        f"Наш {username} настолько крут, что даже бинарный код шепчет ему спасибо!",
        f"{username} — это как антивирус, но для человеческих проблем. И да, он бесплатно не распространяется!",
        f"Когда у нас падает сервер, {username} не бежит — он просто летит на крыльях SSH!",
        f"Спасибо, {username}, за то, что ты — единственная причина, по которой мы не перешли на ‘бумажный офис’!",
        f"{username} знает пароль от матрицы. Но, к счастью, он на нашей стороне!",
        f"Если бы у {username} был криптонит, это были бы неработающие патчи!",
        f"{username} — это как Ctrl+Alt+Del, но для всей нашей компании!",
        f"Наш {username} настолько быстр, что даже пинг ему завидует!",
        f"Спасибо, {username}, за то, что ты — единственный, кто понимает, что ‘это не баг, это фича’ — не шутка!",
        f"{username} не спит. Он просто переходит в режим ожидания!",
        f"Если бы у {username} был девиз, это было бы: ‘Я не волшебник, я просто знаю, где искать логи’!",
        f"{username} — это как облако, но без лишних дождей и с гарантированным аптаймом!",
        f"Наш {username} настолько крут, что даже битые пиксели перед ним извиняются!",
        f"Спасибо, {username}, за то, что ты — единственный, кто может объяснить, почему ‘все работает’ — это не ответ!",
        f"{username} — это как Wi-Fi: когда он рядом, все просто работает. И да, мы его очень ценим!",
    ]
    return random.choice(mess)


def bad_work(username):
    mess = [
        f"{username} решил подарить нам неплохой драматический момент, играя 'Пропал в долгах с задачами'!",
        f"Мы слышали, что {username} начал отдыхать, потому что он закончил все задачи... в своих снах.",
        f"Мы организуем сбор средств для {username} - каждый, кто не отставал от плана, может скинуться на билет в будущее.",
        f"Считаем, что {username} взял на себя роль 'Двигатель экономии времени'. Мы ждем его производительных результатов!",
        f"Думаю, {username} решил устроить тайный мастер-класс 'Как увеличить количество невыполненных задач'.",
        f"Иногда {username} становится таким невидимым, что мы подозреваем, что он исследует науку камуфляжа.",
        f"Новое хобби {username}: не заниматься производительностью... ",
        f"Пока все мы учились решать задачи, {username} мастерил план 'Исчезновения из списка задач'.",
        f"Секрет успеха {username}: делать все медленнее, чем кажется возможным. Так, никто и не заметит!",
        f"Если {username} был бы профессиональным спящим, он был бы богат. Научитесь многому, наблюдая за ним!",
        f"Загадка {username}: почему он всегда такой медленный? Он, возможно, пытается победить в 'Медленном марафоне задач'!",
        f"Важно помнить, что {username} обратил задачу в искусство: искусство не заканчивать ничего.",
        f"Если {username} учился бы на факультете 'Отсрочки и оправдания', он был бы лучшим!",
        f"Мы подозреваем, что {username} работает по плану: 'Завалить всё, чтобы потом чудесно спасти'.",
        f"Секрет {username}: он считает, что лучшая задача - это задача, которую не нужно выполнять.",
        f"Кажется, {username} принял решение пойти на 'Отдыхательскую Олимпиаду' и выиграть золотую медаль в лежании на диване!",
        f"Пока все трудились, {username} исследовал феномен 'Исчезновение с рабочего места'.",
        f"Самый сложный вызов: попробовать понять, как {username} считает, что это нормально.",
        f"Если {username} учился бы в Школе Тормозологии, он был бы профессионалом!",
        f"Серьезное исследование: как {username} умудряется сделать меньше, чем ничего.",
        f"Мы думали, {username} - глава 'Клуба последнего минутчика'. Оказалось, он - единственный член!",
        f"Подсказка для {username}: чтобы сделать что-то, нужно начать сделывать что-то. Попробуйте!",
    ]
    return random.choice(mess)


async def get_stats():
    analyzer = DataAnalyzer(session_maker)
    await analyzer.get_results()
    await analyzer.get_total_open_tickets()

    message, finish = await get_message(analyzer, 'сегодня')
    message += f'\n\nОткрытых заявок осталось: {analyzer.total_open[0][0]}\n\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'
    logger.info(message)
    logger.info(finish)

    # если сегодня воскресенье
    if datetime.datetime.today().weekday() == 6:
        message, finish = get_message(analyzer, 'месяц')
        return message, finish

    # если сегодня последний день месяца
    today = datetime.date.today()
    is_last_day_of_month = today.day == calendar.monthrange(today.year, today.month)[1]
    if is_last_day_of_month:
        message, finish = get_message(analyzer, 'месяц')
        return message, finish

    return message, finish

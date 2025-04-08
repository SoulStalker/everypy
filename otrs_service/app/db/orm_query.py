from sqlalchemy.future import select
from sqlalchemy import func, text, cast, Date
from datetime import datetime

# from database import db
from .models import Ticket, User


class DataAnalyzer:
    def __init__(self, session_maker):
        self.results = None
        self.total_open = None
        self.session_maker = session_maker

    async def get_results(self):
        async with self.session_maker() as session:
            async with session.begin():
                query = select(
                    User.first_name,
                    User.last_name,
                    func.count(Ticket.tn).label('count')
                ).join(
                    Ticket, User.id == Ticket.change_by
                ).filter(
                    Ticket.ticket_state_id.in_([2]),
                    text("CAST(Ticket.change_time AS DATE) = CURRENT_DATE"),
                    Ticket.queue_id.in_([1, 4]),
                    Ticket.change_by.notin_([6, 12])
                ).group_by(
                    User.first_name, User.last_name
                ).order_by(
                    text('count DESC')
                ).limit(100)

                result = await session.execute(query)
                self.results = result.all()

    async def get_total_open_tickets(self):
        async with self.session_maker() as session:
            async with session.begin():
                query = select(
                    func.count(Ticket.tn),
                    func.min(cast(Ticket.change_time, Date))
                ).filter(
                    Ticket.ticket_state_id == 1,
                    Ticket.queue_id.in_([1, 4])
                ).limit(500)

                result = await session.execute(query)
                self.total_open = result.all()

    async def get_month_results(self):
        async with self.session_maker() as session:
            async with session.begin():
                start_month = datetime(datetime.now().year, datetime.now().month, 1)
                end_month = datetime(datetime.now().year, datetime.now().month + 1, 1)

                query = select(
                    User.first_name,
                    User.last_name,
                    func.count(Ticket.tn).label('count')
                ).join(
                    Ticket, User.id == Ticket.change_by
                ).filter(
                    Ticket.ticket_state_id.in_([2]),
                    Ticket.change_time >= start_month,
                    Ticket.change_time < end_month,
                    Ticket.queue_id.in_([1, 4]),
                    Ticket.change_by.notin_([6, 12])
                ).group_by(
                    User.first_name, User.last_name
                ).order_by(
                    text('count DESC')
                ).limit(5000)

                result = await session.execute(query)
                self.results = result.all()


def main():
    """
    Запуск анализа для проверки. Основной запуск из main.py
    :return:
    """
    analyzer = DataAnalyzer()
    analyzer.get_results()
    print(*analyzer.results)
    analyzer.get_total_open_tickets()
    print(*analyzer.total_open)
    analyzer.get_month_results()
    print(*analyzer.results)


if __name__ == '__main__':
    main()

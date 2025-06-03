from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Sequence

from sqlalchemy import select, func, case

from .engine import session_maker  # import session factory
from .models import Shifts, Purchases


async def get_unclosed_shifts(report_day: date = date.today()) -> Sequence[Shifts]:
    """
    Возвращает список незакрытых смен за текущий или предыдущий день.
    """
    async with session_maker() as session:  # автоматически закроет сессию
        query = (
            select(Shifts)
            .where(
                (Shifts.operday >= report_day - timedelta(days=1)) &
                (Shifts.state == 0)
            )
            .order_by(Shifts.shopindex)
        )
        result = await session.execute(query)
        return result.scalars().all()


async def get_results_by_shop(report_day: date = date.today()) -> dict[int, Any]:
    """
    Возвращает словарь с результатами по каждому магазину и общую сводку.
    Формат: {shop_index: {'sum_by_checks': float, 'checks_count': int, 'state': str}, ..., 'total_summary': {...}}
    """
    async with session_maker() as session:
        stmt = (
            select(
                Shifts.shopindex,
                Shifts.cashnum,
                Shifts.numshift,
                Shifts.operday,
                Shifts.state,
                Shifts.inn,
                func.count(
                    case((Purchases.cash_operation == 0, Purchases.checksumstart))
                ).label('check_count'),
                func.sum(
                    case(
                        (Purchases.operationtype, Purchases.checksumend),
                        (~Purchases.operationtype, -Purchases.checksumend)
                    )
                ).label('sum_by_checks')
            )
            .join(Purchases)
            .where(
                Shifts.operday == report_day,
                Purchases.checkstatus == 0
            )
            .group_by(
                Shifts.shopindex,
                Shifts.cashnum,
                Shifts.numshift,
                Shifts.operday,
                Shifts.state,
                Shifts.inn
            )
            .order_by(Shifts.shopindex, Shifts.cashnum)
        )

        result = await session.execute(stmt)
        rows = result.fetchall()

        # Собираем отдельные записи
        results_today = []
        for row in rows:
            results_today.append({
                'shop_index': row[0],
                'cash_num': row[1],
                'num_shift': row[2],
                'operation_day': row[3],
                'state': row[4],
                'inn': row[5],
                'checks_count': row[6],
                'sum_by_checks': float(row[7] / Decimal('100')),
            })

        # Объединяем по магазину
        combined: dict[int, dict[str, Any]] = defaultdict(lambda: {
            'sum_by_checks': 0.0,
            'checks_count': 0,
            'state': set()
        })
        for rec in results_today:
            idx = rec['shop_index']
            combined[idx]['sum_by_checks'] += rec['sum_by_checks']
            combined[idx]['checks_count'] += rec['checks_count']
            combined[idx]['state'].add(rec['state'])

        # Формируем итоговую сводку
        total_summary = {
            'sum_by_checks': sum(v['sum_by_checks'] for v in combined.values()),
            'checks_count': sum(v['checks_count'] for v in combined.values()),
            'state': set()
        }
        for v in combined.values():
            total_summary['state'].update(v['state'])

        combined['total_summary'] = total_summary

        # Приводим state к строке
        result_dict: dict[int, dict[str, Any]] = {}
        for k, v in combined.items():
            result_dict[k] = {
                'sum_by_checks': v['sum_by_checks'],
                'checks_count': v['checks_count'],
                'state': str(v['state'])
            }

        return result_dict

from datetime import datetime, timedelta
from fastapi import FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import *
from database import engine

app = FastAPI(title="Лаба 4")


@app.get('/employees_with_discount')  # Задание №1
def get_employees_with_discount():
    with Session(autoflush=False, bind=engine) as db:
        employees = db.query(Workers).all()
        response = []
        for employee in employees:
            response.append({
                'id': employee.id,
                'name': employee.name,
                'post': employee.post,
                'discount_on_clothes': employee.discount_on_clothes
            })
        result = {'employees': response}
        return result


@app.get('/workwear_types')  # Задание №2
def get_workwear_types():
    with Session(autoflush=False, bind=engine) as db:
        workwear_types = db.query(WorkWear).all()
        response = []
        for workwear in workwear_types:
            response.append({
                'id': workwear.id,
                'clothes_type': workwear.wear_type,
                'period_of_wearing': workwear.period_of_wearing,
                'price': workwear.price
            })
        result = {'workwear_types': response}
        return result


@app.get('/employees_workwear_receipts')  # Задание №3
def get_employees_workwear_receipts():
    with Session(autoflush=False, bind=engine) as db:
        workwear_receipts = db.query(GetGoods, Workers).join(Workers).all()
        response = []
        for record in workwear_receipts:
            response.append({
                'worker_id': record.Workers.id,
                'name': record.Workers.name,
                'clothes_id': record.GetGoods.clothes_id,
                'get_date': record.GetGoods.get_date
            })
        result = {'workwear_receipts': response}
        return result


@app.get('/employees_workwear_replacement')  # Задание №4
def get_employees_workwear_replacement():
    with Session(autoflush=False, bind=engine) as db:
        employees_workwear = db.query(Workers, GetGoods, WorkWear).join(Workers, GetGoods.worker_id == Workers.id).join(
            WorkWear, GetGoods.clothes_id == WorkWear.id).all()
        response = []
        current_date = datetime.now()
        for record in employees_workwear:
            wear_date = record.GetGoods.get_date
            period_of_wearing = record.WorkWear.period_of_wearing
            if (current_date - wear_date).days > period_of_wearing:
                response.append({
                    'worker_id': record.Workers.id,
                    'name': record.Workers.name,
                    'clothes_id': record.GetGoods.clothes_id,
                    'clothes_type': record.WorkWear.wear_type,
                    'last_wear_date': wear_date
                })
        result = {'employees_workwear_replacement': response}
        return result


@app.get('/average_discount_per_department')  # Задание №5
def get_average_discount_per_department():
    with Session(autoflush=False, bind=engine) as db:
        departments = db.query(Workers.post, func.avg(Workers.discount_on_clothes).label('avg_discount')).group_by(
            Workers.post).all()
        average_discounts = {department.post: department.avg_discount for department in departments}
        result = {'average_discount_per_department': average_discounts}
        return result


@app.get('/demand_for_workwear_types')  # Задание №6
def get_demand_for_workwear_types():
    with Session(autoflush=False, bind=engine) as db:
        demand_counts = db.query(GetGoods.clothes_id, func.count(GetGoods.clothes_id).label('count')).group_by(
            GetGoods.clothes_id).all()
        response = []
        for item in demand_counts:
            workwear_type = db.query(WorkWear).filter(WorkWear.id == GetGoods.clothes_id).first()
            response.append({
                'clothes_type': workwear_type.wear_type,
                'demand_count': item.count
            })
        result = {'demand_for_workwear_types': response}
        return result


@app.get('/most_demanded_workwear_per_workshop')  # Задание №7
def get_most_demanded_workwear_per_workshop():
    with Session(autoflush=False, bind=engine) as db:
        workshops = db.query(Workshop).all()
        response = []
        for workshop in workshops:
            workshop_workers = db.query(Workers).filter(Workers.workshop_id == workshop.id).all()
            workshop_demand = {}
            for worker in workshop_workers:
                worker_demands = db.query(GetGoods.clothes_id).filter(GetGoods.worker_id == worker.id).all()
                for demand in worker_demands:
                    if demand.clothes_id in workshop_demand:
                        workshop_demand[demand.clothes_id] += 1
                    else:
                        workshop_demand[demand.clothes_id] = 1
            most_demanded_id = max(workshop_demand, key=workshop_demand.get)
            most_demanded_type = db.query(WorkWear).filter(WorkWear.id == most_demanded_id).first()
            response.append({
                'workshop_name': workshop.workshop_name,
                'most_demanded_workwear': {
                    'clothes_type': most_demanded_type.wear_type,
                    'demand_count': workshop_demand[most_demanded_id]
                }
            })
        result = {'most_demanded_workwear_per_workshop': response}
        return result


@app.get('/workshops_without_workers')  # Задание №8
def get_workshops_without_workers():
    with Session(autoflush=False, bind=engine) as db:
        empty_workshops = db.query(Workshop).filter(~Workshop.id.in_(db.query(Workers.workshop_id))).all()
        response = [{'workshop_name': workshop.workshop_name} for workshop in empty_workshops]
        result = {'workshops_without_workers': response}
        return result

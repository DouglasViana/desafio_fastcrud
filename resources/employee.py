from flask_restful import Resource, reqparse
from models.employee import EmployeeModel
from flask import request, jsonify
from sql_alchemy import datastorage


class Employees(Resource):

    def get(self):
        trab = []
        for employee in EmployeeModel.query.all():
            trab.append(employee.json())
        return {'employees': trab}

    def post(self):

        employee = [request.json['name'], request.json['cpf'], request.json['team_id']]
        new_employee = EmployeeModel(*employee)
        datastorage.session.add(new_employee)
        datastorage.session.commit()

        return jsonify(new_employee.json())




class Employee(Resource):
    info = reqparse.RequestParser()
    info.add_argument('name', type=str, required=True, help="The Field 'name' cannot be left blank")
    info.add_argument('cpf', type=int, required=True, help="The Field 'cpf' cannot be left blank")
    info.add_argument('team', type=str, required=True, help="The Field 'team' cannot be left blank")

    def get(self, employee_id):
        employee = EmployeeModel.find_employee(employee_id)
        if employee:
            return employee.json()
        return {'message': 'Employee not found.'}, 404

    def put(self, employee_id):
        data = Employee.info.parse_args()
        employee_found = EmployeeModel.find_employee(employee_id)
        if employee_found:
            employee_found.update_employee(**data)
            employee_found.save_employee()
            return employee_found.json(), 200
        hotel = EmployeeModel(employee_id, **data)
        try:
            hotel.save_employee()
        except:
            return {'message': 'An internal error occurred trying to save employee.'}, 500
        return hotel.json(), 201


    def delete(self, employee_id):
        employee = EmployeeModel.find_employee(employee_id)
        if employee:
            try:
                employee.delete_employee()
            except:
                return {'message': 'An error occurred trying to delete employee.'}, 500
            return {'message': 'Employee deleted'}
        return {'message': 'Employee not found'}, 404

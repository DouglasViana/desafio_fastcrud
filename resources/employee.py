from flask_restful import Resource, reqparse
from models.employee import EmployeeModel
from flask import request, jsonify
from sql_alchemy import datastorage
import mysql.conector
from dotenv import load_dotenv
import os

load_dotenv()

my_user = os.getenv("USER")
my_password = os.getenv("PASS")
my_host = os.getenv("HOST")
my_database = os.getenv("DATABASE")

def normalize_path_params(employee_id,
                          name,
                          cpf,
                          team,
                          limit=10,
                          offset=0, **workers):
     if limit:
         return {
             'employee_id': employee_id,
             'name': name,
             'cpf': cpf,
             'team': team.json(),
             'limit': limit,
             'offset': offset
         }

path_params = reqparse.RequestParser()
path_params.add_argument('employee_id', type=int)
path_params.add_argument('name', type=str)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Employees(Resource):

    def get(self):
        connection = mysql.connector.connect(user=my_user, password=my_password,
                                             host=my_host,
                                             database=my_database)
        cursor = connection.cursor()

        workers = path_params.parse_args()
        workers_valid = {chave:workers[chave] for chave in workers if workers[chave] is not None}
        parametros = normalize_path_params(**workers_valid)

        if parametros.get('limit'):
            query = "SELECT * FROM employees \
                    LIMIT %s OFFSET %s"
            tupla = tuple([parametros[chave]for chave in parametros])
            cursor.execute(query, tupla)
            result = cursor.fetchall()

        trab = []
        if result:
            for row in result:
                trab.append({
                    'employee_id': row[0],
                    'name': row[1],
                    'cpf': row[2],
                    'team': row[3]
                })

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

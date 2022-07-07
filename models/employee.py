from sql_alchemy import datastorage
from sqlalchemy import ForeignKey
from models.team import TeamModel


class EmployeeModel(datastorage.Model):
    __tablename__ = 'employees'

    employee_id = datastorage.Column(datastorage.Integer, primary_key=True)
    name = datastorage.Column(datastorage.String(80))
    cpf = datastorage.Column(datastorage.String(80))
    team_id = datastorage.Column(datastorage.Integer, ForeignKey('team.team_id'))
    team = datastorage.relationship(TeamModel)


    def __init__(self, name, cpf, team_id):
        self.name = name
        self.cpf = cpf
        self.team_id = team_id

    def json(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'cpf': self.cpf,
            'team': self.team.json()
        }

    @classmethod
    def find_employee(cls, employee_id):
        employee = cls.query.filter_by(employee_id=employee_id) .first()
        if employee:
            return employee
        return None

    def save_employee(self):
        datastorage.session.add(self)
        datastorage.session.commit()


    def update_employee(self, name, city, team_id):
        self.name = name
        self.city = city
        self.team_id = team_id

    def delete_employee(self):
        datastorage.session.delete(self)
        datastorage.session.commit()

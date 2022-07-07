from sql_alchemy import datastorage
from sqlalchemy import ForeignKey
from models.employee import EmployeeModel


class RecommendationModel(datastorage.Model):
    __tablename__ = 'recommendations'

    recommendation_id = datastorage.Column(datastorage.Integer, primary_key=True)
    name = datastorage.Column(datastorage.String(80))
    email = datastorage.Column(datastorage.String(80))
    employee_id = datastorage.Column(datastorage.Integer, ForeignKey('employees.employee_id'))
    employee = datastorage.relationship(EmployeeModel)

    def __init__(self, recommendation_id, name, email, employee_id):
        self.recommendation_id = recommendation_id
        self.name = name
        self.email = email
        self.employee_id = employee_id

    def json(self):
        return {
            'recommendation_id': self.recommendation_id,
            'name': self.name,
            'email': self.email,
            'employee_id': self.employee_id,
            'employee': self.employee

        }

    @classmethod
    def find_recommendation(cls, recommendation_id):
        recommendation = cls.query.filter_by(recommendation_id=recommendation_id).first()
        if recommendation:
            return recommendation
        return None

    def save_recommendation(self):
        datastorage.session.add(self)
        datastorage.session.commit()


    def update_recommendation(self, name, email, employee_id):
        self.name = name
        self.email = email
        self.employee_id = employee_id

    def delete_recommendation(self):
        datastorage.session.delete(self)
        datastorage.session.commit()

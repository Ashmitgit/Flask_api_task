from flask import request, jsonify, abort
from . import db
from .models import Employee
from . import create_app

app = create_app()

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(
        name=data['name'],
        email=data['email'],
        position=data['position'],
        salary=data['salary']
    )
    db.session.add(new_employee)
    db.session.commit()

    # Simulating the external API call and response
    # In a real scenario, you should use requests.post() to call the external API
    external_api_response = {'id': new_employee.id, 'created_on': str(new_employee.created_on)}

    new_employee.id = external_api_response['id']
    new_employee.created_on = datetime.fromisoformat(external_api_response['created_on'])
    db.session.commit()

    return jsonify(new_employee.to_dict()), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.json

    employee.name = data.get('name', employee.name)
    employee.email = data.get('email', employee.email)
    employee.position = data.get('position', employee.position)
    employee.salary = data.get('salary', employee.salary)

    db.session.commit()
    return jsonify(employee.to_dict())

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204

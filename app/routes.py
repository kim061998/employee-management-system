from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from .models import User, Employee
from . import db

UPLOAD_FOLDER = 'app/static/Emp_photo'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
routes = Blueprint('routes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('routes.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@routes.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.query.all()
    departments = db.session.query(Employee.department).distinct().all()
    return render_template('dashboard.html', employees=employees, departments=departments)

@routes.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        try:
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            employee = Employee(
                id=request.form['id'],  # Ensure ID is provided
                name=request.form['name'],
                position=request.form['position'],
                department=request.form['department'],
                contact=request.form['contact'],
                date_of_birth=date_of_birth,
                address=request.form['address']  # Get address from form
            )
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                employee.photo = filename
            db.session.add(employee)
            db.session.commit()
            flash('Employee added successfully', 'success')
            return redirect(url_for('routes.dashboard'))
        except Exception as e:
            db.session.rollback()
            return render_template('add_employee.html', error=str(e))
    return render_template('add_employee.html')

@routes.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        try:
            employee.name = request.form['name']
            employee.position = request.form['position']
            employee.department = request.form['department']
            employee.contact = request.form['contact']
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth:
                employee.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            employee.address = request.form['address']  # Update address
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                employee.photo = filename
            db.session.commit()
            flash('Employee updated successfully', 'success')
            return redirect(url_for('routes.dashboard'))
        except Exception as e:
            db.session.rollback()
            return render_template('edit_employee.html', employee=employee, error=str(e))
    return render_template('edit_employee.html', employee=employee)

@routes.route('/delete_employee/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        if employee.photo:
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], employee.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        db.session.delete(employee)
        db.session.commit()
        if request.method == 'DELETE':
            return {'success': True, 'message': 'Employee deleted successfully'}, 200
        flash('Employee deleted successfully', 'success')
        return redirect(url_for('routes.dashboard'))
    except Exception as e:
        db.session.rollback()
        if request.method == 'DELETE':
            return {'success': False, 'message': str(e)}, 500
        flash('Error deleting employee', 'danger')
        return redirect(url_for('routes.dashboard'))

@routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            current_user.username = request.form['username']
            if request.form['password']:
                current_user.set_password(request.form['password'])
            current_user.role = request.form['role']
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('routes.profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile', 'danger')
    return render_template('profile.html', admin=current_user)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('routes.login'))

@routes.route('/view_employee/<int:id>', methods=['GET'])
@login_required
def view_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('view_employee.html', employee=employee)

@routes.route('/manage_employee')
@login_required
def manage_employee():
    employees = Employee.query.all()
    return render_template('manage_employee.html', employees=employees)

@routes.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

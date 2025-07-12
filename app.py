from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from flask_restful import Api, Resource, reqparse
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmaster.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
api = Api(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
@login_required
def add():
    content = request.form['content']
    due_date_str = request.form['due_date']
    category = request.form['category']
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
    new_task = Task(content=content, due_date=due_date, category=category, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
@login_required
def complete(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return redirect(url_for('index'))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


class TaskResource(Resource):
    @login_required
    def get(self, task_id=None):
        if task_id:
            task = Task.query.get_or_404(task_id)
            if task.user_id != current_user.id:
                return {'message': 'Unauthorized'}, 403
            return jsonify({
                'id': task.id,
                'content': task.content,
                'completed': task.completed,
                'category': task.category,
                'due_date': task.due_date.isoformat() if task.due_date else None
            })
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': task.id,
            'content': task.content,
            'completed': task.completed,
            'category': task.category,
            'due_date': task.due_date.isoformat() if task.due_date else None
        } for task in tasks])

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('category', type=str)
        parser.add_argument('due_date', type=str)
        args = parser.parse_args()

        new_task = Task(
            content=args['content'],
            category=args['category'],
            due_date=datetime.strptime(args['due_date'], '%Y-%m-%d') if args['due_date'] else None,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            'id': new_task.id,
            'content': new_task.content,
            'completed': new_task.completed,
            'category': new_task.category,
            'due_date': new_task.due_date.isoformat() if new_task.due_date else None
        }), 201

    @login_required
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            return {'message': 'Unauthorized'}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        parser.add_argument('completed', type=bool)
        parser.add_argument('category', type=str)
        parser.add_argument('due_date', type=str)
        args = parser.parse_args()

        if args['content']:
            task.content = args['content']
        if args['completed'] is not None:
            task.completed = args['completed']
        if args['category']:
            task.category = args['category']
        if args['due_date']:
            task.due_date = datetime.strptime(args['due_date'], '%Y-%m-%d')

        db.session.commit()
        return jsonify({
            'id': task.id,
            'content': task.content,
            'completed': task.completed,
            'category': task.category,
            'due_date': task.due_date.isoformat() if task.due_date else None
        })

    @login_required
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            return {'message': 'Unauthorized'}, 403
        db.session.delete(task)
        db.session.commit()
        return '', 204


api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

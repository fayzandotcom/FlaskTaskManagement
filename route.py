from app import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from forms import AddTaskForm, DeleteTaskForm
from models import Task
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    task_list = Task.query.all()
    return render_template('index.html', tasks = task_list)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    add_form = AddTaskForm()
    if add_form.validate_on_submit():
        task = Task(title = add_form.title.data, date = datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('index'))
    else:
        return render_template('add.html', form = add_form)

@app.route('/edit/<int:task_id>', methods = ['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    edit_form = AddTaskForm()

    if task:
        if edit_form.validate_on_submit():
            task.title = edit_form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash ('Task updated successfully!')
            return redirect(url_for('index'))
        else:
            edit_form.title.data = task.title
            return render_template('edit.html', form = edit_form, task_id = task_id)
    else:
        flash('Task not found!')
        return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods = ['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    delete_form = DeleteTaskForm()

    if task:
        if delete_form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash ('Task deleted successfully!')
            return redirect(url_for('index'))
        else:
            return render_template('delete.html', form = delete_form, task_id = task_id, title = task.title)
    else:
        flash('Task not found!')
        return redirect(url_for('index'))
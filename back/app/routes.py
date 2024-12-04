from flask import Blueprint, render_template, redirect, url_for, request
from .models import Event
from .forms import EventForm
from . import db
from datetime import datetime
import matplotlib.pyplot as plt
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            estimated_budget=form.estimated_budget.data,
            actual_spent=form.actual_spent.data
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_event.html', form=form)

@main.route('/compare')
def compare():
    events = Event.query.filter(Event.date < datetime.now().date()).all()
    labels = [e.title for e in events]
    estimated = [e.estimated_budget or 0 for e in events]
    actual = [e.actual_spent or 0 for e in events]

    plt.bar(labels, estimated, alpha=0.6, label='Estimated')
    plt.bar(labels, actual, alpha=0.6, label='Actual', color='orange')
    plt.legend()
    plt.title('Comparison: Estimated vs Actual')
    plt.savefig('static/comparison.png')
    plt.close()

    return render_template('compare.html', image='static/comparison.png')

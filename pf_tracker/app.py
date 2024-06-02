from flask import Flask, render_template, request, redirect, url_for, Markup, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import pandas as pd
from pandas import Period
import matplotlib.pyplot as plt
import seaborn as sns

import io
import base64



from personal_finance import PersonalFinance

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLO999BLUD666'


class ExpenseForm(FlaskForm):
    # date entry
    date = DateField('DATE', format='%Y-%m-%d', validators=[DataRequired()])

    # category entry
    category = SelectField('CATEGORY',
                           choices=[('living', 'LIVING🏡'), ('food', 'FOOD🍔'), ('transport', 'TRANSPORT🚗'), ('fun', 'FUN😹'),
                                    ('education', 'EDUCATION🤓'), ('savings', 'SAVINGS🤑')], validators=[DataRequired()])

    # title of expense entry
    title = StringField('TITLE', validators=[DataRequired()])

    # amount entry
    amount = FloatField('AMOUNT', validators=[DataRequired()])

    # optional notes
    notes = TextAreaField('NOTES')

    # submit button
    submit = SubmitField('ADD')

class DeleteForm(FlaskForm):
    index = IntegerField('INDEX', validators=[DataRequired()])
    confirm = SubmitField('CONFIRM DELETE')

personal_finance = PersonalFinance('user')
try:
    personal_finance.load()
except AssertionError:
    print('no data found for {}'.format(personal_finance.name))

@app.route('/', methods=['GET', 'POST'])
def index():
    month = request.args.get('month')
    if month != 'ALL':
        month = Period(month, 'M')
    form = ExpenseForm()
    if form.validate_on_submit():
        date = str(form.date.data)
        category = form.category.data
        title = form.title.data
        amount = form.amount.data
        notes = form.notes.data if form.notes.data else " "
        personal_finance.new_entry(date, category, title, amount, notes)
        personal_finance.dump()
        return redirect(url_for('index'))

    # month selector
    months = ['ALL'] + list(set(personal_finance._temp_data['month']))

    month_data = personal_finance.monthly_cat_totals(month = month)
    print(month_data)

    if not month_data.empty:
        plt.figure(figsize=(8, 4))
        sns.set_theme(style='dark')
        sns.barplot(data=month_data, x = 'amount', y = 'category', width=0.5)
        plt.title(month)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plot_url = 'data:image/png;base64,{}'.format(plot_url)

    else:
        plot_url = None

    return render_template('index.html', form=form, months=months, plot_url=plot_url)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        index = delete_form.index.data
        try:
            personal_finance.delete_index(index)
            personal_finance.dump()
            flash(f'{index} deleted', 'success')
        except IndexError:
            flash(f'UHHH', 'danger')
        return redirect(url_for('expenses'))

    return render_template('expenses.html', delete_form=delete_form, expenses=personal_finance.data.to_dict('records'))


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.197')

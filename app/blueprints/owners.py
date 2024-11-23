from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

owners = Blueprint('owners', __name__)

# Route to display owner details and add a new owner
@owners.route('/owner', methods=['GET', 'POST'])
def owner():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new owner
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Insert the new owner into the owners table
        cursor.execute('INSERT INTO owners (first_name, last_name) VALUES (%s, %s)',
                       (first_name, last_name))
        db.commit()

        flash('New owner added successfully!', 'success')
        return redirect(url_for('owners.owner'))

    # Handle GET request to display all owners (this part should remain if you want to display all owners)
    cursor.execute('SELECT * FROM owners')
    all_owners = cursor.fetchall()
    return render_template('owners.html', all_owners=all_owners)

# Route to update an owner's details
@owners.route('/update_owner/<int:owner_id>', methods=['GET', 'POST'])
def update_owner(owner_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the owner's details
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        cursor.execute('UPDATE owners SET first_name = %s, last_name = %s WHERE owners_id = %s',
                       (first_name, last_name, owner_id))
        db.commit()

        flash('Owner updated successfully!', 'success')
        return redirect(url_for('owners.owner'))

    # GET method: fetch owner's current data for pre-populating the form
    cursor.execute('SELECT * FROM owners WHERE owners_id = %s', (owner_id,))
    current_owner = cursor.fetchone()
    return render_template('update_owner.html', current_owner=current_owner)

# Route to delete an owner
@owners.route('/delete_owner/<int:owner_id>', methods=['POST'])
def delete_owner(owner_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the owner
    cursor.execute('DELETE FROM owners WHERE owners_id = %s', (owner_id,))
    db.commit()

    flash('Owner deleted successfully!', 'danger')
    return redirect(url_for('owners.owner'))

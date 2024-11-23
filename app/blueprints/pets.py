from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

pets = Blueprint('pets', __name__)

# Route to display pet details and add a new pet
@pets.route('/pet', methods=['GET', 'POST'])
def pet():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new pet
    if request.method == 'POST':
        pet_name = request.form['pet_name']
        pet_age = request.form['pet_age']
        owner_id = request.form['owner_id']  # Assuming owner_id is selected from a list of owners

        # Insert the new pet into the pets table
        cursor.execute('INSERT INTO pets (pet_name, pet_age, owner_id) VALUES (%s, %s, %s)',
                       (pet_name, pet_age, owner_id))
        db.commit()

        flash('New pet added successfully!', 'success')
        return redirect(url_for('pets.pet'))

    # Handle GET request to display all pets along with owner's first and last name
    cursor.execute('''
        SELECT pets.pet_id, pets.pet_name, pets.pet_age, owners.first_name, owners.last_name, pets.owner_id
        FROM pets
        JOIN owners ON pets.owner_id = owners.owners_id
    ''')
    all_pets = cursor.fetchall()

    # Fetch all owners for the dropdown list
    cursor.execute('SELECT owners_id, first_name, last_name FROM owners')
    all_owners = cursor.fetchall()

    return render_template('pets.html', all_pets=all_pets, all_owners=all_owners)

# Route to update a pet's details
@pets.route('/update_pet/<int:pet_id>', methods=['GET', 'POST'])
def update_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the pet's details
        pet_name = request.form['pet_name']
        pet_age = request.form['pet_age']
        owner_id = request.form['owner_id']

        cursor.execute('UPDATE pets SET pet_name = %s, pet_age = %s, owner_id = %s WHERE pet_id = %s',
                       (pet_name, pet_age, owner_id, pet_id))
        db.commit()

        flash('Pet updated successfully!', 'success')
        return redirect(url_for('pets.pet'))

    # GET method: fetch pet's current data for pre-populating the form
    cursor.execute('SELECT * FROM pets WHERE pet_id = %s', (pet_id,))
    current_pet = cursor.fetchone()

    # Fetch all owners for the dropdown list
    cursor.execute('SELECT owners_id, first_name, last_name FROM owners')
    all_owners = cursor.fetchall()

    return render_template('update_pet.html', current_pet=current_pet, all_owners=all_owners)

# Route to delete a pet
@pets.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the pet
    cursor.execute('DELETE FROM pets WHERE pet_id = %s', (pet_id,))
    db.commit()

    flash('Pet deleted successfully!', 'danger')
    return redirect(url_for('pets.pet'))


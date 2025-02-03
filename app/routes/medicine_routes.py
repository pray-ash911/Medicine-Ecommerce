from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app import db
from models.medicine_model import Medicine
from testify import app
from utils.role_required import role_required
import os


medicine_blueprint = Blueprint('medicine', __name__, template_folder='../templates')

# Set the upload folder to store images
UPLOAD_FOLDER = 'static/images/medicines'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@medicine_blueprint.route('/', methods=['GET'])
#@role_required('Admin')
def view_medicines():
    page = request.args.get('page', 1, type=int)
    medicines = Medicine.query.paginate(page=page, per_page=9)  # Adjust per_page as desired
    return render_template('view_medicines.html', medicines=medicines)

@medicine_blueprint.route('/add', methods=['GET', 'POST'])
#@role_required('Admin')
def add_medicine():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        discount = request.form.get('discount')

        # Retrieve the uploaded image
        image = request.files.get('image')
        if image and image.filename != '':
            # Secure the filename and save it
            filename = secure_filename(image.filename)
            # Save image in 'static/images/medicines/' directory
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                image.save(image_path)
                # Save only the relative path in the database
                image_url = f"images/medicines/{filename}"
            except Exception as e:
                flash(f"Error saving image: {e}", "error")
                return redirect(url_for('medicine.add_medicine'))
        else:
            flash("Please upload an image for the medicine.", "error")
            return redirect(url_for('medicine.add_medicine'))

        # Save the medicine record in the database
        new_medicine = Medicine(
            name=name,
            description=description,
            price=price,
            stock=stock,
            discount=discount,
            image_url=image_url
        )
        db.session.add(new_medicine)
        db.session.commit()
        flash("Medicine added successfully!", "success")
        return redirect(url_for('medicine.view_medicines'))

    return render_template('add_medicine.html')


@medicine_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
#@role_required('Admin')
def edit_medicine(id):
    medicine = Medicine.query.get_or_404(id)
    if request.method == 'POST':
        medicine.name = request.form['name']
        medicine.description = request.form['description']
        medicine.price = request.form['price']
        medicine.stock = request.form['stock']
        medicine.discount = request.form.get('discount', 0.0)

        # Handle image upload if a new file is uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:  # Check if there’s an actual file
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                # Update the medicine image_url
                medicine.image_url = f'images/medicines/{filename}'

        db.session.commit()
        flash('Medicine updated successfully!', 'success')
        return redirect(url_for('medicine.view_medicines', id=medicine.id))  # Ensure ID is included
    return render_template('update_medicine.html', medicine=medicine)


@medicine_blueprint.route('/delete/<int:id>', methods=['POST'])
#@role_required('Admin')
def delete_medicine(id):
    medicine = Medicine.query.get_or_404(id)

    # Delete the image file associated with the medicine
    if medicine.image_url:
        image_path = os.path.join(app.root_path, medicine.image_url)  # Construct the absolute path
        try:
            os.remove(image_path)
        except OSError:
            flash("Error deleting the image file.", "error")

    db.session.delete(medicine)
    db.session.commit()
    flash("Medicine deleted successfully!", "success")
    return redirect(url_for('medicine.view_medicines'))


from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .models import Note,User
from web_app import db
import json

front = Blueprint('front', __name__, template_folder='templates')

# home page route
@front.route('/')
@front.route('/home')
def home():
  return render_template("home.html", user=None)

# route for redirecting user to their notes and start creating
@front.route('/mynotes', methods=['GET', 'POST'])
@login_required
def mynotes():
  if request.method == 'POST':
    note = request.form.get('note')
    if len(note) < 1:
      flash("The note is too short", category='error')
    else:
      new_note = Note(data=note, date=func.now(), user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      flash("Note created", category='success')
  return render_template("mynotes.html", user=current_user)

# route to redirect currently logged in use to their profile
@front.route('/profile')
def profile():
  return render_template('profile.html', user=current_user)

# route for deleting a note
@front.route('delete_note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
      flash("Note successfully deleted", category='success')
  return jsonify({})

# route for editing a note
@front.route('edit_note', methods=['POST'])
@login_required
def edit_note():
  
  note_data = request.get_json()
  note_id = note_data['noteId']
  updated_content = note_data['newContent']

  note = Note.query.get(note_id)
  if note and note.user_id == current_user.id:
    note.data = updated_content
    db.session.commit()
    flash("Note successfully updated", category='success')
  
  return jsonify({})

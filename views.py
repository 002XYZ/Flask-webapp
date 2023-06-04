# Here we define the differnts paths the user might go when they open the website,
# like the homepage, the login page, etc. 
from flask import render_template,request,flash,jsonify
from flask_login import login_required,current_user
from .models import Note
from . import db
import json
from flask import Blueprint  # This means this file is a blueprint of our application,
                             # it has a bunch of urls/routes inside of it, so that we 
                             # don't have all our views in one file, we can find in many files
views=Blueprint('views',__name__)                             

@views.route('/',methods=['GET','POST'])  # This is a decorator. This what it does is whenever there is '/' after
        # the website url, it will directly run this function, basically the homepage
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) == 0:
            flash('Note is too short!',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            flash('Note added successfully!',category='success')
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html',user=current_user) # When homepage is called, home.html will be displayed/rendered
                            # we will be able to reference current user and check if it's authenticated 

@views.route('/delete-note', methods=['POST'])
def delete_note():                
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            delete.session.delete(note) # this is how to delete from database
            db.session.commit()
    return jsonify({})
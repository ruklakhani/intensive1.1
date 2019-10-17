
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.Playlister
playlists = db.playlists

# app.py
# OUR MOCK ARRAY OF PROJECTS
# playlists = [
#    { 'title': 'music video slappers', 'description': 'dope music with dope visuals' },
#    { 'title': 'fave videos', 'description': 'videos I enjoy' }
# ]


@app.route('/')
def playlist_index():
   
    """Show all playlists."""
    return render_template('playlist_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlist_new():

    """Create a new playlist."""
    return render_template('playlist_new.html', playlist={}, title='New Playlist')


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    
    """Submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'rating': request.form.get('rating')
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlist_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>')
def playlist_show(playlist_id):
   
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlist_show.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlist_index'))

if __name__ == '__main__':
    app.run(debug=True)

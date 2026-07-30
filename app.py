import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'erb_services_secret_key'

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista slika za početnu animaciju pozadine (slider)
BG_IMAGES = ['bg1.png', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg', 'bg5.jpg']

# Inicijalna galerija slika (može se proširivati preko admin panela)
gallery_images = ['bg1.png', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg', 'bg5.jpg']

@app.route('/')
def index():
    return render_template('index.html', bg_images=BG_IMAGES)

@app.route('/dienstleistungen')
def dienstleistungen():
    return render_template('dienstleistungen.html', bg_images=BG_IMAGES)

@app.route('/warum-wir')
def warum_wir():
    return render_template('warum_wir.html', bg_images=BG_IMAGES)

@app.route('/galerie')
def galerie():
    return render_template('galerie.html', images=gallery_images, bg_images=BG_IMAGES)

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html', bg_images=BG_IMAGES)

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '123456':
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Falsches Passwort!')
    return render_template('admin_login.html')

# Admin Dashboard za dodavanje slika
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                gallery_images.append(filename)
                return redirect(url_for('admin_dashboard'))
                
    return render_template('admin_dashboard.html', images=gallery_images)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
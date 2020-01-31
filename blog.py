from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap

import urllib
import os

from ristoranti import ristoranti
from itinerari import itinerari
from testi import pagine

app = Flask(__name__)
Bootstrap(app)


@app.route("/itinerari/<int:indice>/")
def caricaItinerario(indice):
    return render_template("blog_itinerario.html", itinerario=itinerari[indice])


@app.route("/itinerari/")
def mostraItinerari():
    return render_template("blog_itinerari.html", itinerari=itinerari)




@app.route("/")
def presentazione():
    return render_template("blog_content.html", pagina=pagine["presentazione"])


@app.route("/aeroporti/")
def aeroporti():
    return render_template("blog_content.html", pagina=pagine["aeroporti"])


@app.route("/come_muoversi/")
def come_muoversi():
    return render_template("blog_content.html", pagina=pagine["come_muoversi"])


@app.route("/inner_book/<quartiere>/")
def caricaLibroRistorante(quartiere):
    return render_template("blog_restaurant.html", quartiere=quartiere)

@app.route("/ristoranti/")
def mostra_ristoranti():
    # (900,550) dimensione del book al 100%
    ord_ristoranti = list(ristoranti.keys())
    ord_ristoranti.sort()
    return render_template("blog_restaurants.html", ristoranti= ord_ristoranti)
    #return book("marais")



@app.route("/book/<quartiere>/")
def book(quartiere):
    print("In book:%s" % quartiere);
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template("book2.html", ristoranti=ristoranti[quartiere], countRest=len(ristoranti[quartiere]),
                           quartiere=quartiere, myvideo=myvideo)


@app.route("/ristoranti/<quartiere>/<int:n>/")
def restaurants(quartiere,n):
    r = ristoranti[quartiere]
    print("Ristoranti del %s\n\n" % quartiere)
    if (n==0):
        return render_template('rest_page_front_title.html', rist=r[0])

    #elif (n==len(r)-1 and n%2==1):
    #    return render_template('rest_page_back.html', rist=r[n-1])

    elif (n%2==1):
        return render_template('rest_page_left.html', rist=r[int((n - 1) / 2)])
    else:
        return render_template('rest_page_right_images.html', rist=r[int((n-2) / 2)])



@app.route("/collage/")
def collage():
    return redirect(url_for("static", filename="collage/index.html"))



@app.route("/video/<quartiere>/<int:n>/")
def video(quartiere,n):
    r = ristoranti[quartiere]
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template('rest_page_right.html', rist=r[n], myvideo=myvideo)


@app.route("/editor/")
def page_editor():
    #send_from_directory("static", 'itinerari/itinerario_01.html')
    f = open("static/itinerari/itinerario_01.html", "r")
    content = f.read()
    f.close()
    return render_template("page_editor.html", content=content)


#
# FILE UPLOAD CODE
#
#https://stackoverflow.com/questions/44926465/upload-image-in-flask
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/uploaded_images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploaded/<filename>/")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action="/upload/">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host="192.168.0.118" , port=5000, debug=True)
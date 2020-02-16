from flask import Flask,  Blueprint, render_template, request, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
import os
from .models import Page
from . import db

from .ristoranti import ristoranti
from .itinerari import itinerari
from .testi import pagine


main = Blueprint('main', __name__,template_folder='templates',static_folder='static')

#https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
#https://stackoverflow.com/questions/54733662/how-to-send-html-data-to-flask-without-form


@main.route("/itinerari/<int:indice>/")
def caricaItinerario(indice):
    return render_template("blog_itinerario.html", itinerario=itinerari[indice])


@main.route("/itinerari/")
def mostraItinerari():
    return render_template("blog_itinerari.html", itinerari=itinerari)




@main.route("/")
def presentazione():
    return render_template("blog_content.html", pagina=pagine["presentazione"])


@main.route("/aeroporti/")
def aeroporti():
    return render_template("blog_content.html", pagina=pagine["aeroporti"])


@main.route("/come_muoversi/")
def come_muoversi():
    return render_template("blog_content.html", pagina=pagine["come_muoversi"])


@main.route("/inner_book/<quartiere>/")
def caricaLibroRistorante(quartiere):
    return render_template("blog_restaurant.html", quartiere=quartiere)

@main.route("/ristoranti/")
def mostra_ristoranti():
    # (900,550) dimensione del book al 100%
    ord_ristoranti = list(ristoranti.keys())
    ord_ristoranti.sort()
    return render_template("blog_restaurants.html", ristoranti= ord_ristoranti)
    #return book("marais")



@main.route("/book/<quartiere>/")
def book(quartiere):
    print("In book:%s" % quartiere);
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template("book2.html", ristoranti=ristoranti[quartiere], countRest=len(ristoranti[quartiere]),
                           quartiere=quartiere, myvideo=myvideo)


@main.route("/ristoranti/<quartiere>/<int:n>/")
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



@main.route("/collage/")
def collage():
    return redirect(url_for("static", filename="collage/index.html"))



@main.route("/video/<quartiere>/<int:n>/")
def video(quartiere,n):
    r = ristoranti[quartiere]
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template('rest_page_right.html', rist=r[n], myvideo=myvideo)


@main.route("/editor/")
@login_required
def page_editor():
    #send_from_directory("static", 'itinerari/itinerario_01.html')
    print(os.getcwd())
    #print(url_for("static", filename="itinerari/itinerario_01.html"))

    f = open("./project/static/itinerari/itinerario_01.html", "r")
    content = f.read()
    f.close()
    return render_template("page_editor.html", content=content)

@main.route("/save/", methods=["POST"])
def save_page():
    form_data = request.form['content']
    index = request.form.get('menu_index')
    menu_title = request.form.get('menu_title')
    print("Salvo con menu %s e indice %s" % (menu_title, index))

    # restituisce il path completo dove salvare il file
    filenameToSave = add_page_to_db(menu_title=menu_title,index=index)
    if filenameToSave!=None:
        #print("Content:\n%s" % str(form_data))
        print("Percorso di salvataggio:%s" % filenameToSave)
        f = open(filenameToSave, "w")
        f.write(form_data)
        f.close()
        return "Pagina salvata (%s)" % filenameToSave
    return "Si sono verificati problemi nel salvare la pagina."



def getPageFilename(name):
    return "%s.html " % name.replace("'","").lower().replace(".","_").replace(" ","_").replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')

def add_page_to_db(menu_title, index, page_id=None):
    try:
        if page_id==None:
            # create new page with the form data. Hash the password so plaintext version isn't saved.
            filename= getPageFilename(menu_title)
            path = "./project/static/menu_pages/%s" % filename
            new_page = Page(menu_title=menu_title,path=path, index=int(index))

            # add the new page to the database
            db.session.add(new_page)
            db.session.commit()
            return path

    except Exception as ex:
        print("Eccezione nella scrittura della pagina sul db:%s" % ex)
        raise ex
        return None

    return None
#
# FILE UPLOAD CODE
#
#https://stackoverflow.com/questions/44926465/upload-image-in-flask
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/uploaded/<filename>/")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@main.route('/upload/', methods=['GET', 'POST'])
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
            return redirect(url_for("main.uploaded_file", filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action="/upload/">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


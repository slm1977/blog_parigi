from flask import Flask,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
import os
from .models import Page
from . import db
from .db_queries import get_pages, add_page_to_db, update_page

pages = Blueprint('pages', __name__,template_folder='templates',static_folder='static')

@pages.route("/create/")
@login_required
def create_new_page():
    return page_edit()


@pages.route("/load_page/<page_id>/")
def load_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    f = open(page.path, "r")
    content = f.read()
    f.close()
    pagina = {"contenuto" : content}
    return render_template("blog_content.html", pagina=pagina, menu=get_pages(), page_id=page_id)


@pages.route("/sort_pages/")
@login_required
def sort_pages():
    return render_template("page_sorting.html", pages=get_pages())

@pages.route("/edit/<page_id>/")
@login_required
def page_edit(page_id=None):
    #send_from_directory("static", 'itinerari/itinerario_01.html')
    #print(url_for("static", filename="itinerari/itinerario_01.html"))
    if page_id==None or int(page_id)<0:
        return render_template("page_editor.html", content="", page=None)
    else:
        page = Page.query.filter_by(id=page_id).first()
        f = open(page.path, "r")
        content = f.read()
        f.close()
        return render_template("page_editor.html", content=content, page=page)


@pages.route("/save/", methods=["POST"])
def save_page():
    form_data = request.form['content']
    index = request.form.get('menu_index')
    menu_title = request.form.get('menu_title')
    print("Salvo con menu %s e indice %s" % (menu_title, index))

    # crea una nuova pagina sul db e restituisce il path completo dove salvare il file
    filenameToSave = add_page_to_db(menu_title=menu_title,index=index)
    # il file viene creato solo se la pagina è stata aggiunta correttamente sul db
    if filenameToSave!=None:
        #print("Content:\n%s" % str(form_data))
        print("Percorso di salvataggio:%s" % filenameToSave)
        f = open(filenameToSave, "w")
        f.write(form_data)
        f.close()
        result = {"success" : True, "message" : "Pagina salvata (%s)" % filenameToSave }
        return jsonify(result)
    result = {"success": False, "message": "Si sono verificati problemi nel salvare la pagina."}
    return jsonify(result)



def getPageFilename(name):
    return "%s.html " % name.replace("'","").lower().replace(".","_").replace(" ","_").replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')

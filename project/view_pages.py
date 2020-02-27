from flask import Flask,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
import os
import time
from .models import Page
from . import db
from .db_queries import get_pages, add_page_to_db, update_page, delete_page, update_pages_index

pages = Blueprint('pages', __name__,template_folder='templates',static_folder='static')

@pages.route("/create/")
@login_required
def create_new_page():
    return page_edit()


@pages.route("/load_menu_page/<menu_page_index>/")
def load_menu_page(menu_page_index):
    try:
        page = get_pages()[int(menu_page_index)]
        print("Trovata pagina:%s" % page)
        if page==None:
            raise Exception("Impossibile trovare la pagina di menu n.%s" % menu_page_index)
        return load_page(page.id)
    except Exception as ex:
        print ("load_menu_page Exception:%s" % ex)
        return redirect("/")

@pages.route("/load_page/<page_id>/")
def load_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    f = open(page.path, "r")
    content = f.read()
    f.close()
    pagina = {"contenuto" : content}
    return render_template("blog_content.html", pagina=pagina, menu=get_pages(), page_id=page_id)


@pages.route("/sort_pages/", methods=["GET", "POST"])
@login_required
def sort_pages():
    if request.method=="GET":
        pages_id = []
        pages = get_pages()
        for p in pages:
            pages_id.append(p.id)
        return render_template("page_sorting.html", pages=pages, pages_id=pages_id)
    else:
        pages_id = request.form['pages_id']
        print("ID PAGINE DA AGGIORNARE:")
        print(pages_id)
        result = update_pages_index(pages_id)
        return jsonify(result)



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
@login_required
def save_page():
    form_data = request.form['content']
    menu_title = request.form.get('menu_title')
    page_id = request.form.get('id')
    visible = request.form.get('visible')
    print("Salvo con menu %s" % menu_title)

    if page_id==None or int(page_id)<0:
        # crea una nuova pagina sul db e restituisce il path completo dove salvare il file
        filenameToSave = add_page_to_db(menu_title=menu_title, visible=visible)
    else:
        # aggiorna la pagina preesistente
        filenameToSave = update_page(page_id,menu_title, visible)

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


@pages.route("/delete/<page_id>")
@login_required
def remove_page(page_id):
    print("RIMOZIONE PAGINA:%s" % page_id)
    # rimuovo la pagina dal db
    filepath = delete_page(page_id)
    if filepath!=None:
        newfile_path = "%s_deleted_%s" % (filepath, int(time.time()))
        os.rename(filepath, newfile_path)
    return redirect("/")

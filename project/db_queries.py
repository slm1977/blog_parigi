from . import db
from .models import Page

def get_pages():
    pages = Page.query.order_by(Page.index).all()
    for p in pages:
        print(p.menu_title)
    return pages

def add_page_to_db(menu_title, index=None, page_id=None):
    try:
        if index==None:
            index = Page.query.count()
        if page_id==None:
            # create new page with the form data. Hash the password so plaintext version isn't saved.
            last_id = Page.query.order_by(Page.id.desc()).first().id
            filename= "page_%s.html" % (last_id+1)
            path = "./project/static/menu_pages/%s" % filename
            new_page = Page(menu_title=menu_title,path=path, index=int(index))

            # add the new page to the database
            db.session.add(new_page)
            db.session.commit()
            return path

    except Exception as ex:
        print("Eccezione nella scrittura della pagina sul db:%s" % ex)
        #raise ex
        return None

    return None

def update_page(page_id, new_menu_title):
    page = Page.query.get(page_id)
    page.menu_title = new_menu_title
    db.session.commit()
    return page.path


def update_pages_index(id_list):
    try:
        for i in range(len(id_list)):
            page = Page.query.get(id_list[i])
            if page:
                page.index = (i+1)
                db.session.commit()
        result = {"success": True, "message": "Ordine delle pagine aggiornato"}
        return result
    except Exception as ex:
        print("Eccezione salvataggio ordinamento:%s" % ex)
        db.session.rollback()
        result =  {"success": False, "message": "Eccezione salvataggio ordinamento:%s" % ex}
        return result


def delete_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    if page==None:
        return None
    filepath = page.path
    print("Sto rimuovendo la pagina con id:%s" % page.id)
    db.session.query(Page).filter(Page.id == page.id).delete(synchronize_session=False)
    db.session.commit()
    print("Pagina rimossa")
    return filepath











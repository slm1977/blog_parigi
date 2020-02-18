from . import db
from .models import Page

def get_pages():
    pages = Page.query.order_by(Page.index).all()
    for p in pages:
        print(p.menu_title)
    return pages

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
        #raise ex
        return None

    return None


def update_pages_index(id_list):
    for i in range(len(id_list)):
        page = Page.query.get(id_list[0])
        page.index = (i+1)
        db.session.commit()




def update_page(page_id, new_path, new_index, new_menu_title):
    if page_id<0:
        return
    page = Page.query.get(page_id)
    page.menu_title = new_menu_title
    page.path = new_path
    page.index = new_index
    db.session.commit()







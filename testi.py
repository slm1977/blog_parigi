faccia_con_cuori="1f60d"
faccia_che_ride = "1f601"
occhiolino = "1f609"

def em(code):
    return """<img height="20" src="https://pic.sopili.net/pub/emoji/twitter/2/72x72/%s.png" width="20" />""" % code

presentazione= """
Ciao a tutti mi presento: io sono Micky e innanzi tutto amo Parigi ..che ve lo dico a fare %s sono proprio innamorata pazza di questa citta’ %s  ,dal primo momento in cui l’ho vista,proprio come un colpo di fulmine e da allora non andrei piu’ da nessun’altra parte per il “piacere” del mio compagno. 

Ci siamo stati diverse volte ormai ma Parigi è come un oceano. "Gettateci una sonda e non ne conoscerete mai la profondità", diceva Balzac... Non si finisce mai di conoscerla.

Per cui l’idea di questo blog e’ dedicata soprattutto agli amici che spesso mi hanno chiesto consigli su questa meravigliosa citta’ e che devono visitarla per la prima volta.. o al massimo per la seconda %s

Vi daro’ qualche consiglio su come organizzare al meglio il vostro soggiorno e qualche dritta per non spendere un patrimonio e godervi al massimo e con comodita’ il vostro soggiorno, riuscendo a vedere le cose a mio parere da non perdere assolutamente, e per i piu’ curiosi o per chi ha intenzione di tornarci piu volte anche qualche suggerimento per una Parigi più insolita e meno turistica.

Se vorrete inoltre potrete contattarmi sul Blog per avere dei consigli personalizzati: sara’ un piacere per me aiutarvi e, insieme ad altri amici, compreso tu che leggi, potrai aiutare in futuro con la tua esperienza parigina altri viaggiatori che stanno per partire nella “nostra” amata citta’, perche’ sono certa che anche tu farai parte del club degli innamorati pazzi come me!

E allora che aspetti...buona lettura e ..buon viaggio %s
""" % (em(faccia_che_ride), em(faccia_con_cuori),em(occhiolino), em(occhiolino))

pagine = {"presentazione" : {
                                "titolo" : "Presentazione",
                                "contenuto" : presentazione,
                                "image" : "fotoblog/presentazione.jpg"
                            }
        }



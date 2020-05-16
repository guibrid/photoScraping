#DELETE FILES IN FOLDER AND DELETE ENTRY IN DB BASED ON THE NAME OF THE FILE

import os
import mysql.connector


def productList(gencod):
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    query = ("SELECT id FROM products WHERE gencod= "+ gencod +"")
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def deletePhoto(idProduct):
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    query = ("DELETE FROM photos WHERE product_id= %s" % (idProduct))
    cursor.execute(query)
    cnx.commit()
    return True

liste = os.listdir()

for item in liste:
    if item != 'list.py':
        gencod = item.replace('.jpg', '')
        print('GENCOD:' + str(gencod))
        for productId in productList(gencod):
            print('- '+ str(productId[0]))
            if( deletePhoto(productId[0]) ):
                try:
                    os.remove(item)
                except Exception as e:
                    print("Fichier deja supprimer")
                
                




import csv
from urllib import request
import mysql.connector
#with open('gencod.csv') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')

def productList(gencod):
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    query = ("SELECT id FROM products WHERE gencod= "+ gencod +"")
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def photoList(productIds):
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    #query = ("SELECT id FROM photos WHERE product_id IN ({0})".format(
    #', '.join(['%s'] * len(productIds))))
    #cursor.execute(query, productIds)
    query = ("SELECT id FROM photos WHERE product_id= %s" % (productIds))
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def insertPhoto(idProduct, gencod):
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    imageFile = str(gencod) + '.jpg'
    query = "INSERT INTO photos (url, product_id, type, active) VALUES (%s, %s, 0, 2)"
    val = (imageFile, idProduct)
    cursor.execute(query, val)
    cnx.commit()
    print( 'Nouvelle photo ajouté')

def updatePhoto(idPhoto, gencod):
    print(str(idPhoto) + '-'+ str(gencod))
    cnx = mysql.connector.connect(user='root', password='', database='cake_crmsci')
    cursor = cnx.cursor()
    imageFile = str(gencod) + '.jpg'
    query = "UPDATE photos SET url = %s, active = %s WHERE id = %s"
    val = (imageFile, 2, idPhoto)
    cursor.execute(query, val)
    cnx.commit()
    print( 'Photo mise à jour')



for line in open("gencod.csv"):
    csv_row = line.split() #returns a list ["1"]
    photoURL = 'https://photos.groupesafo.com/wsse/cb8f190153190ebe8598ac49e86ebf37/800/800/' + str(csv_row[0])
    f = open('photos/'+ str(csv_row[0]) +'.jpg', 'wb')
    f.write(request.urlopen(photoURL).read())
    f.close()

    # List les Id produits qui on se gencod
    idProduits = productList(str(csv_row[0]))

    for idProduit in idProduits:
        print('ID du GENCOD ' + str(csv_row[0]) + ': ' + str(idProduit[0]))
       
        if idProduit:
            print('List des Id produits qui ont ce gencod: ' + str(idProduit[0]))
            # Rechercher si les produits ont deja une photo
            idPhotos = photoList(idProduit[0])
            # Si oui update l'url de la photo par le nom du fichier et mettre active à 2
            if idPhotos:
                print(idPhotos[0][0])
                updatePhoto(idPhotos[0][0], str(csv_row[0]))
            # Si non Ajouter dans la table photos 'nom du fichier' , 'product_id', 0 , 2
            else:
                print('Pas de photo')
                insertPhoto(idProduit[0], str(csv_row[0]))

    

    
    #break
         
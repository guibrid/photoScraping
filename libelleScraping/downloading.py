# SRAPPING PHOTO FROM SOGEDIAL WEBSITE

from urllib import request
from urllib import error
import mysql.connector
from PIL import Image, ImageChops, ImageOps


def updatePhoto(idPhoto, gencod):
    cursor = cnx.cursor()
    imageFile = str(gencod) + '.jpg'
    query = "UPDATE photos SET url = %s WHERE id = %s"
    val = (str(imageFile), idPhoto)
    cursor.execute(query, val)
    cnx.commit()

def resizeImg(imgFile):
    basewidth = 1024
    img = Image.open(imgFile)
    if(img.size[1] > basewidth or img.size[0] > basewidth):
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(imgFile)





cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='cake_crmsci')
cursor = cnx.cursor()

query = ("SELECT url, code, gencod, photos.id FROM products, photos WHERE photos.active = 2  AND photos.product_id = products.id AND url LIKE '%http%' LIMIT 2000")

cursor.execute(query)
rows = cursor.fetchall()



for photo in rows:
    #print(photo[0])
    print('id Photo: '+str(photo[3]))
    photoURL= photo[0]
    #photoURL = 'https://photos.groupesafo.com/wsse/cb8f190153190ebe8598ac49e86ebf37/800/800/' + str(photo[2])
    #print(photoURL)

    #f = open('photos/4008713700923-0.jpg', 'wb')
    #f.write(request.urlopen(photoURL).read())
    #exit()



    #break
    try:
        conn = request.urlopen(photoURL)
    except error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
        print('HTTPError: {}'.format(e.code))
        print('id Photo: '+str(photo[3]))
        print('-----------------------------')
    except error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))
        print('id Photo: '+str(photo[3]))
        print('-----------------------------')
    else:
        
        file_ext = '.'+photoURL.split('.')[-1]
        file_ext = file_ext.split('?', 1)[0]

        f = open('photos/'+ str(photo[2]) + file_ext, 'wb')
        f.write(request.urlopen(photoURL).read())
        f.close()
        #Resize image
        resizeImg('photos/'+ str(photo[2]) + file_ext)
        # Update url base
        updatePhoto(str(photo[3]), str(photo[2]))
        print('product GENCOD: ' + str(photo[2]) + ' | ' + 'id photo:' + str(photo[3]) + ' | OK')
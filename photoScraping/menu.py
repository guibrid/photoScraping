## Text menu in Python
from urllib import request
from urllib import error
import mysql.connector
from PIL import Image, ImageChops, ImageOps
import ftplib
import os

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='cake_crmsci')
cnx.cursor()

def getPhotoExt(url):
    file_ext = '.'+url.split('.')[-1]
    file_ext = file_ext.split('?', 1)[0]
    return file_ext

def photoListQuery(cursor):
    query = ("SELECT url, code, gencod, photos.id FROM products, photos WHERE photos.active = 2  AND photos.product_id = products.id AND url LIKE '%http%'")
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def resizeImg(imgFile):
    basewidth = 1024
    img = Image.open(imgFile)
    if(img.size[1] > basewidth or img.size[0] > basewidth):
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(imgFile)

def updatePhoto(cnx, cursor, idPhoto, gencod):
    imageFile = str(gencod) + '.jpg'
    query = "UPDATE photos SET url = %s WHERE id = %s"
    val = (str(imageFile), idPhoto)
    cursor.execute(query, val)
    cnx.commit()

def ftpUpload():
    session = ftplib.FTP_TLS('sgp63.siteground.asia','guibrid@worldlinkadvance.com','ty%o7E&^k7-^') #FTP Connexion
    session.cwd('/public_html/app/scinternational/scifiles/assets/')  # Change difrectory           
    for photo in os.listdir("photos"):             # Loop through the file in /photos/ folder
        file = open('photos/'+photo,'rb')          # open file to send
        session.storlines('STOR '+photo, file)     # send the file
        file.close()                               # close file
    print('All files uploaded')

def download(photosList):
    for photo in photosList:

        print('id Photo: '+str(photo[3]))
        photoURL= photo[0]   
        try:
            request.urlopen(photoURL)
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

            ext = getPhotoExt(photoURL) #Get photo extension
            #Create a new file and save new photo
            f = open('photos/'+ str(photo[2]) + ext, 'wb')
            f.write(request.urlopen(photoURL).read())
            f.close()
            #Resize image
            resizeImg('photos/'+ str(photo[2]) + ext)
            # Update url base
            updatePhoto(cnx, cnx.cursor(), str(photo[3]), str(photo[2]))
            print('product GENCOD: ' + str(photo[2]) + ' | ' + 'id photo:' + str(photo[3]) + ' | OK')


def print_menu():
    print ()
    print ("SC INTERNATIONAL : Photo download script")
    print ('----------------------------------------')
    print ("1. Downloading photo and resize it")
    print ("2. Upload picture on scifiles application")
    print ("3. Update database on scifiles with new pictures")
    print ("5. Exit")
    print ("")
  
loop=True      
  
while loop:          ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = int(input("Enter your choice [1-5]: "))
    
     
    if choice==1:     
        print ("Menu 1 has been selected")
        photoList = photoListQuery(cnx.cursor())
        download(photoList)
        ## You can add your code or functions here
    elif choice==2:
        print ("Upload picture on scifiles application")
        ## You can add your code or functions here
        ftpUpload()
    elif choice==3:
        print ("Update database on scifiles with new pictures")
        ## You can add your code or functions here
    elif choice==5:
        print ("Menu 5 has been selected")
        ## You can add your code or functions here
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Enter any key to try again..")
# EXTRACT HYPERLINK FROM EXCEL CEL

from openpyxl import load_workbook
import urllib.request 


wb = load_workbook(filename = 'photos.xlsx')
sheet_ranges = wb['Sheet1']
colA = 'A'
colB = 'B'

for x in range(1, 2):

    colB +=str(x)
    colA +=str(x)
    print('Extraction du lien de la celulle: '+ colB)
    print(sheet_ranges[colB].hyperlink.target)
    picurl =sheet_ranges[colB].hyperlink.target
    picname = str(sheet_ranges[colA].value) + '.jpg'
    print(picurl + ' - ' + picname)
    #urllib.request.urlretrieve(picurl, picname)
    print('-----------------------------------')
    colB = 'B'
    colA = 'A'
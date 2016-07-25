"""mapping fuctions: excel to dic"""

from openpyxl import load_workbook
import pprint
wb = load_workbook(filename = '/Users/efgallegos/Dropbox/Automation/Bankers/bankers_product_matrix.xlsx')
sheet_annuity = wb['annuity']

annuity_matrix = {}

row = 6
while True:
    if sheet_annuity['C'+str(row)].value == None:
        #print (sheet_annuity['C'+str(row)].value)
        break
    else:
        col = 'D'
        while True:
            if sheet_annuity[col + '5'].value == None:
                #print(sheet_annuity[col + '5'].value)
                break
            else:
                if sheet_annuity[col + str(row)].value == 'x':
                    if sheet_annuity['C' + str(row)].value in annuity_matrix:
                        annuity_matrix[sheet_annuity['C' + str(row)].value].append(sheet_annuity[col + '5'].value)
                    else:
                        annuity_matrix[sheet_annuity['C' + str(row)].value] = [sheet_annuity[col + '5'].value]
                col = chr(ord(col) + 1) 
    row += 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(annuity_matrix)


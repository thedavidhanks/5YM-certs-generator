import csv
import json
import os.path
from export_pdf import FiveYrCertMaker

'''


'''

# Test code to avoid asking for filename. Comment out for production
def getData(filename):
    with open(filename, 'r', encoding='utf-8-sig', newline='') as data:
        # Ask user for target CSV filename
        # filename = input('Enter target CSV file name: ')
        # Open target CSV file and load to csv Reader object
        # with open(filename, 'r', encoding='utf-8-sig', newline='') as data:
        readCSV = csv.reader(data, delimiter=',', quoting=csv.QUOTE_ALL)
        # Convert reader object to list of rows
        output = [row for row in readCSV]
    # Send each row to make Word Document
    return output

def certNum(number):
    if len(number) == 1:
        number = '00' + number
        return number
    elif len(number) == 2:
        number = '0' + number
        return number
    else:
        return number



if __name__ == "__main__":
    # Ask user for file names

    # Hard coded filenames for test. Comemented out in production
    # jobFilename = 'jobdata.json'
    # certFilename = 'testdata.csv'
    
    ''' Production request for filenames to target'''
    jobDataInputQ = 'Enter the target JSON file name for JOB DATA [jobdata.json]: '
    defaultJsonFile = 'jobdata.json'
    jobFilename = input(jobDataInputQ)
    if not jobFilename:
        jobFilename = defaultJsonFile
    while not os.path.isfile('CSVdata/'+jobFilename):
        print(jobFilename+' could not be found.  Try again')
        jobFilename = input(jobDataInputQ)
        if not jobFilename:
            jobFilename = defaultJsonFile
    print(jobFilename+' located')
    certFilename = input('Enter the target CSV file name for EQUIPMENT DATA: ')
    while not os.path.isfile('CSVdata/'+certFilename):
        print(certFilename+' could not be found.  Try again.')
        certFilename = input('Enter the target CSV file name for EQUIPMENT DATA: ')
    print('You entered:  ' + certFilename)

    # Collect data from files
    #jobdata = getData('CSVdata/'+jobFilename)[0]
    with open('CSVdata/'+jobFilename) as file:
        jobdata = json.load(file)

    # Open certification file
    certData = getData('CSVdata/'+certFilename)
    # print(certData)
    # print(jobdata)
    x = 0
    while x != len(certData):
        certPackage = certData[x]
        # print(certPackage)
        doc = FiveYrCertMaker('output/'+jobdata['project'] + '_C' + certNum(certPackage[0]) + ' - ' + certPackage[2] + '.pdf', jobdata, certPackage)
        doc.createDocument()
        doc.savePDF()
        x += 1
    print('Total certificates created: ' + str(x))
    print('Conversion process is complete')





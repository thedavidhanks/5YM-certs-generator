import csv
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
    # jobFilename = 'jobdata.csv'
    # certFilename = 'testdata.csv'

    ''' Production request for filenames to target'''
    jobFilename = input('Enter the target CSV file name for JOB DATA: ')
    print('You entered:  ' + jobFilename)
    certFilename = input('Enter the target CSV file name for CERTIFICATION DATA: ')
    print('You entered:  ' + certFilename)

    # Collect data from files
    jobdata = getData('CSVdata/'+jobFilename)[0]

    # Open certification file
    certData = getData('CSVdata/'+certFilename)
    # print(certData)
    # print(jobdata)
    x = 0
    while x != len(certData):
        certPackage = certData[x]
        # print(certPackage)
        doc = FiveYrCertMaker('output/'+jobdata[0] + '_C' + certNum(certPackage[0]) + ' - ' + certPackage[2] + '.pdf', jobdata, certPackage)
        doc.createDocument()
        doc.savePDF()
        x += 1
    print('Total certificates created: ' + str(x))
    print('Conversion process is complete')





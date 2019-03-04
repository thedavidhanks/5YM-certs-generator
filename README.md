# 5 YEAR MAINTENACE CERTIFICATE GENERATOR

This generates certificates for 5 year maintenance required by the Code of Federal Regulations.

1. Install python 3.7 or higher ([download](https://www.python.org/downloads/))
2. Install [pip](https://pypi.org/project/pip/)
3. Install [reportlab](https://pypi.org/project/reportlab/)
~~~
lab pip install reportlab
~~~
4. Clone the repository
5. Update the jobdata.json file within the CSVdata
6. Create an equipment.csv within CSVdata folder (format below)
7. from the command line run runCertMaker.py  (python runCertMaker.py)
8. Follow the prompts
9. Files will be in output folder

## equipment.csv
each row of the equipment.csv shall be formatted as follows:  
id,equipment name, GSI#, OEM, OEM Model#, OEM Serial #, Pressure rating, Inspection Procedure

EX.  equipment.csv  
6,	DOUBLE WING: 2" 1502 15M,	20284,	FMC,	3257099,	09230800W017,	15M,	QMSF-2041-5Y  
7,	DOUBLE WING: 2" 1502 15M,	19165,	MSI,	DA0071,	A486171,	15M,	QMSF-2041-5Y  
9,	DOUBLE WING: 2" 1502 15M,	7798,	FMC,	3257099,	09240200W019,	15M,	QMSF-2041-5Y

## jobdata.json
Example jobdata.json
~~~~
{
    "project": "5YM_GSI_190107",
    "revision": "00",
    "clientName": "Gulfstream Services Inc.",
    "releaseDate": "8-Jan-19",
    "inspectionLocation": "Houma Rental Facility",
    "clientTechnicians": ["Edward Skinner","Joseph Allen","Justin Neil"],
    "OTCwitness": {
        "name": "John Griffitt",
        "signatureFile": "sigGriffitt.png"
    },
    "OTCapprover": {
        "name": "David Hanks",
        "signatureFile": "sigHanks.png"
    }
}
~~~~

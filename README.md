#5 YEAR MAINTENACE CERTIFICATE GENERATOR

This generates certificates for 5 year maintenance required by the Code of Federal Regulations.

1. Clone the repository,
2. Update the signatures,
3. Supply a jobdata.csv and equipment.csv
4. run csv_import.py  (python csv_import.py)

equipment.csv shall be formatted as follows:
id,equipment name, GSI#, OEM, OEM Model#, OEM Serial #, Pressure rating, Inspection Procedure

EX.  equipment.csv
6,	DOUBLE WING: 2" 1502 15M,	20284,	FMC,	3257099,	09230800W017,	15M,	QMSF-2041-5Y
7,	DOUBLE WING: 2" 1502 15M,	19165,	MSI,	DA0071,	A486171,	15M,	QMSF-2041-5Y
9,	DOUBLE WING: 2" 1502 15M,	7798,	FMC,	3257099,	09240200W019,	15M,	QMSF-2041-5Y

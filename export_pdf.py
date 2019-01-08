from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY, TA_LEFT
import collections
import datetime

# testdata = ['016', '10F', 'X141516', 'Kemper', 'I1502PJIE', '3520', '15M', 'Trace Type', 'Trace ID',
#             'Trace Date', 'Conformance', 'H2S', 'Procedure']
# jobdata = ['5YM_GSI_179999', '02', 'Gulfstream Services, Inc.', '14 SEP 2007', 'Houma Rental Tools Facility',
#            ['Edward Skinner', 'Alan Ledet'], ['Ben Madison', 'Lloyd Pittman']]

myStyle = ParagraphStyle(
    name='HeaderStyle',
    fontname='Arial',
    fontSize=8,
    alignment=TA_RIGHT,
)
TitleStyle = ParagraphStyle(
    name='TitleStyle',
    fontname='Arial',
    fontSize=14,
    alignment=TA_CENTER,
    textColor=HexColor(0x8b2027)
)

TableStyle = ParagraphStyle(
    name='TableStyle',
    fontname='Arial',
    fontSize=10,
    textColor=colors.black

)

TableHeaderStyle = ParagraphStyle(
    name='TableHeaderStyle',
    fontname='Arial',
    fontSize=10,
    textColor=colors.white

)
########################################################################
class FiveYrCertMaker(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, pdf_file, job, data):
        self.c = canvas.Canvas(pdf_file, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
        self.organization = job['clientName']
        self.job = job['project']
        self.report = self.certNum(data[0])
        self.revision = job['revision']
        self.jobdata = job
        self.certdata = data

        '''
        Job specific data entry for signature blocks
        '''
        self.Witness = job['OTCwitness']['name']
        self.Engineering = job['OTCapprover']['name']

    # ----------------------------------------------------------------------
    def createDocument(self):
        """"""
        voffset = 30

        # create header data
        header = """<font size="9">
        5 Year Maintenance Certificate<br/>
        %s_C%s<br/>
        Rev%s</font>
        """ % (self.job, self.report, self.revision)
        p = Paragraph(header, myStyle)

        # create header logo and size it
        logo = Image("img/image1.jpeg")
        logo.drawHeight = 0.75 * inch
        logo.drawWidth = 2.64 * inch

        # combine logo and header data into array for table creation
        data = [[logo, p]]

        # create table for placement in header region, and define location
        table = Table(data, colWidths=4 * inch)
        table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                        ("VALIGN", (-1, -1), (-1, -1), "CENTER"),
                        ("ALIGN", (-1, -1), (-1, -1), "RIGHT")])
        table.wrapOn(self.c, self.width-100, self.height)
        table.drawOn(self.c, *self.coord(5, 25, mm))

        # create Certificate title
        ptext = "<b>Certificate of Inspection & Compatibility</b>"
        self.createParagraph(ptext, 0, voffset + 8, TitleStyle)

        # create body text of the certificate and style
        ptext = """
        <b><i>OTC Solutions, LLC</i></b> was present for the following 5 Year Maintenance Inspection as
         required in the <i>Code of Federal Regulations</i> requirement per <b>30 CFR §250.739 (b)</b>. 
         The inspections were conducted per <b>%s’s</b> Preventative Maintenance (PM) program and the equipment 
         manufacture’s guidelines.
        """ % self.organization
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.c, self.width - 70, self.height)
        p.drawOn(self.c, *self.coord(15, voffset + 25, mm))

        # create first table
        # create data structure for table parsing
        data = self.dataPrepTable1(self.jobdata, self.certdata)
        table = Table(data, colWidths=3.6 * inch)
        table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                        ('BACKGROUND', (0, 0), (0, 0), HexColor(0x3a3b3d)),
                        ('BACKGROUND', (0, 7), (0, 7), HexColor(0x595959)),
                        ('SPAN', (0, 0), (1, 0)),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(15, voffset + 80, mm))

        # create second table
        data = self.dataPrepTable2(self.certdata)
        table = Table(data, colWidths=3.6 * inch)
        if len(self.certdata[1]) > 45:
            table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                            ("ALIGN", (0, 0), (0, 0), "CENTER"),
                            ('BACKGROUND', (0, 0), (0, 0), HexColor(0x3a3b3d)),
                            ('SPAN', (0, 0), (1, 0)),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('FONTSIZE', (1, 1), (1, 1), 8),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        else:
            table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                            ("ALIGN", (0, 0), (0, 0), "CENTER"),
                            ('BACKGROUND', (0, 0), (0, 0), HexColor(0x3a3b3d)),
                            ('SPAN', (0, 0), (1, 0)),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(15, voffset + 130, mm))

        # # create third table
        # data = self.dataPrepTable3(self.certdata)
        # table = Table(data, colWidths=3.6 * inch)
        # table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
        #                 ("ALIGN", (0, 0), (0, 0), "CENTER"),
        #                 ('BACKGROUND', (0, 0), (0, 0), HexColor(0x3a3b3d)),
        #                 ('SPAN', (0, 0), (1, 0)),
        #                 ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        #                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
        # table.wrapOn(self.c, self.width, self.height)
        # table.drawOn(self.c, *self.coord(15, voffset + 167, mm))

        # create signature area (table)
        data = [['Witness:', self.Witness, 'Date:', datetime.date.today().strftime('%d %b %Y')],
                [],
                ['Engineering Approval:', self.Engineering, 'Date:', datetime.date.today().strftime('%d %b %Y')]
                ]
        table = Table(data, colWidths=(1.5 * inch, 3.75 * inch, 0.6 * inch, 1.35 * inch))
        table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                        ("ALIGN", (0, 0), (0, 1), "RIGHT"),
                        ("ALIGN", (1, 0), (1, 2), "RIGHT")
                        ])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(15, voffset + 200, mm))

        # add in signatures
        logo = Image("img/signatures/sigGriffitt.png")
        logo.drawHeight = .5 * inch
        logo.drawWidth = 1.5 * inch
        logo.wrapOn(self.c, self.width, self.height)
        logo.drawOn(self.c, *self.coord(65, voffset + 187, mm))

        logo = Image("img/signatures/sigHanks.png")
        logo.drawHeight = .5 * inch
        logo.drawWidth = 1.5 * inch
        logo.wrapOn(self.c, self.width, self.height)
        logo.drawOn(self.c, *self.coord(65, voffset + 202, mm))

        # create footer area (table)
        data = [['www.otc-solutions.com', 'PROPRIETARY/CONFIDENTIAL', '1']]
        table = Table(data, colWidths=(2.7 * inch, 2.7 * inch, 2.7 * inch))
        table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                        ("ALIGN", (1, 0), (1, 0), "CENTER"),
                        ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),
                        ])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(5, voffset + 245, mm))
        self.drawLine()

    # ----------------------------------------------------------------------

    def drawLine(self):
        self.c.setLineWidth(0.3)
        # Draw witness signature lines
        self.c.line(52 * mm, 62 * mm, 149 * mm, 62 * mm)
        self.c.line(160 * mm, 62 * mm, 190 * mm, 62 * mm)
        # Draw engineering signature lines
        self.c.line(52 * mm, 50 * mm, 149 * mm, 50 * mm)
        self.c.line(160 * mm, 50 * mm, 190 * mm, 50 * mm)

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height - y * unit
        return x, y

    # ----------------------------------------------------------------------

    def createParagraph(self, ptext, x, y, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))

    # ----------------------------------------------------------------------

    def tableHeading(self, ptext, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        return p

    # ----------------------------------------------------------------------

    def smalltext(self, ptext, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        return p

    # ----------------------------------------------------------------------

    def savePDF(self):
        """"""
        self.c.save()

    # ----------------------------------------------------------------------

    def dataPrepTable1(self, jobinfo, info):
        data = [[self.tableHeading('<b>Inspection Data</b>', TableHeaderStyle), ''],
                [self.tableHeading('<b>Equipment Owner</b>'), self.organization],
                [self.tableHeading('<b>Date(s) of Inspection</b>'), jobinfo['releaseDate']],
                [self.tableHeading('<b>Inspection Location</b>'), jobinfo['inspectionLocation']],
                [self.tableHeading('<b>Technician(s)</b>'), self.techNameFromJson(jobinfo)],
                [self.tableHeading('<b>3rd Party Witness</b>'), jobinfo['OTCwitness']['name']],
                [self.tableHeading('<b>Inspection Procedure Performed</b>'), info[7]],
                [self.tableHeading('<b>5 Year Maintenance Report</b>', TableHeaderStyle), jobinfo['project']+'_5YR']
                ]
        return data

    # ----------------------------------------------------------------------

    def dataPrepTable2(self, info):
        data = [[self.tableHeading('<b>Equipment Data</b>', TableHeaderStyle), ''],
                [self.tableHeading('<b>Description</b>'), info[1]],
                [self.tableHeading('<b>Owner ID</b>'), info[2]],
                [self.tableHeading('<b>OEM</b>'), info[3]],
                [self.tableHeading('<b>OEM Model/Assembly #</b>'), info[4]],
                [self.tableHeading('<b>OEM Serial #</b>'), info[5]],
                [self.tableHeading('<b>Rated Working Pressure</b>'), info[6]]
                ]
        return data

    # def dataPrepTable3(self, info):
    #     data = [[self.tableHeading('<b>Equipment Trace Data</b>', TableHeaderStyle), ''],
    #             [self.tableHeading('<b>MFG Trace ID (WO/COC/MTR)</b>'), info[8]],
    #             [self.tableHeading('<b>Trace Date</b>'), info[9]],
    #             [self.tableHeading('<b>Conformance (e.g. API, NACE, ASME)</b>'), info[10]],
    #             [self.tableHeading('<b>H2S Qualification</b>'), info[11]]
    #             ]
    #     return data

    def desData(self, dataIn):
        dictData = {
            '2" - 10F': 'STRAIT: 2" x 10\' 1502 15MX',
            '2" - 5F': 'STRAIT: 2" x 5\' 1502 15MX',
            '2" - DW': 'DOUBLE WING: 2" 1502 15MX',
            '2" - DT': 'DOUBLE THREAD: 2" 1502 15MX',
            '2" - Y': 'WYE: 2" 1502 15MX',
            '2" - T': 'TEE: 2" 1502 15MX',
            '2" - 90': 'BLOCK 90: 2" 1502 15MX',
            '2" - SWV': 'SWIVEL: 2" 1502 15MX',
            '2"x1"': 'PLUG VALVE: 2" x 1" 1502 15MX',
            '2"x2"': 'PLUG VALVE: 2" x 2" 1502 15MX',
            '2" - Bleed': 'BLEEDER SUB: 2" 1502 15MX',
            '2" - Check': 'DART-TYPE CHECK VALVE: 2" 1502 15MX'
        }
        dictData = collections.defaultdict(lambda: 'MISSING', dictData)
        out = dictData[dataIn[1]]
        if out == 'MISSING':
            print('\n\nERROR! Equipment Type missing on Certificate # ' + dataIn[0] + '\n\n')
        return out

    def procedureData(self, dataIn):
        dictData = {
            '2" - 10F': 'QMSF-2041-5Y',
            '2" - 5F': 'QMSF-2041-5Y',
            '2" - DW': 'QMSF-2041-5Y',
            '2" - DT': 'QMSF-2041-5Y',
            '2" - Y': 'QMSF-2041-5Y',
            '2" - T': 'QMSF-2041-5Y',
            '2" - 90': 'QMSF-2041-5Y',
            '2" - SWV': 'QMSF-2002-5Y',
            '2"x1"': 'QMSF-2003-5Y',
            '2"x2"': 'QMSF-2003-5Y',
            '2" - Bleed': 'QMSF-2041-5Y',
            '2" - Check': 'QMSF-2041-5Y'
        }
        dictData = collections.defaultdict(lambda: 'MISSING', dictData)
        out = dictData[dataIn[1]]
        if out == 'MISSING':
            print('\n\nERROR! Equipment Type missing on Certificate # ' + dataIn[0] + '\n\n')
        return out
    
    def techNameFromJson(self, dataIn):
        out = ''
        for name in dataIn['clientTechnicians']:
            if out == '':
                out = name
            else:
                out += ', ' + name
        return out

    def certNum(self, number):
        if len(number) == 1:
            number = '00' + number
            return number
        elif len(number) == 2:
            number = '0' + number
            return number
        else:
            return number

            # if __name__ == "__main__":
#     doc = FiveYrCertMaker(jobdata[0]+'_C'+testdata[0]+' - ' + testdata[2]+'.pdf', jobdata, testdata)
#     doc.createDocument()
#     doc.savePDF()
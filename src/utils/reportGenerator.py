# Python Program to generate a text file
from fpdf import FPDF
import src.utils.constants as CONST
from datetime import datetime

def generateReport( projectName, platform, date, transcript, compDesc):
    print('GR: generating report')
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', size=16)
    pdf.cell(200, 10, txt=projectName, ln=1, align='C')

    # Project Details
    pdf.set_font('Arial', size=14)
    pdf.cell(200, 10, txt="Project Details", ln=2, align='L')
    pdf.set_font('Arial', size=10)
    pdf.cell(20, 10, txt="Platform: ", ln=0, align='L')
    pdf.cell(100, 10, txt=platform, ln=1, align='L')
    pdf.cell(20, 10, txt="Date: ", ln=0, align='L')
    pdf.cell(100, 10, txt=date, ln=1, align='L')


    # Transcript
    pdf.set_font('Arial', size=14)
    pdf.cell(100, 10, txt="Transcript", ln=1, align='L')
    pdf.set_font('Arial', size=10)
    pdf.multi_cell(200, 10, txt=transcript, align='L')

    # Summary
    pdf.set_font('Arial', size=14)
    pdf.cell(200, 10, txt="Summary", ln=1, align='L')
    pdf.set_font('Arial', size=10)
    pdf.cell(25, 10, txt="Component", ln=0, align='L')
    pdf.cell(100, 10, txt="Description", ln=0, align='L')
    pdf.cell(25, 10, txt="Sentiment", ln=1, align='L')

    for component in compDesc:
        for desc in compDesc[component]:
            pdf.cell(25, 10, txt=component, ln=0, align='L')
            pdf.cell(100, 10, txt=desc['sentence'], ln=0, align='L')
            pdf.cell(25, 10, txt=desc['sentiment'], ln=1, align='L')


    # Write the pdf output into report.pdf file after append date and time
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    reportPath = CONST.REPORT_FOLDER_PATH + "/report" + dt_string + '.pdf'
    pdf.output(reportPath)
    print('GR: Finished generating report')

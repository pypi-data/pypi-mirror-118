import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .gen_base_pdf import GenBasePdf
from .. import services
from ..result_summary import ResultSummary


# -------------------
class GenTpPdf(GenBasePdf):
    # -------------------
    def __init__(self, protocols):
        self._protocols = protocols
        path = os.path.join(services.cfg.outdir, 'tp_results.pdf')
        self._doc_init(path)

    # -------------------
    def gen(self):
        self._gen_test_run_details()
        self._gen_title('Test Protocols with results')

        for protocol in self._protocols:
            # TODO delete
            # p = Paragraph('TODO paragraph before the table?', self._style_sheet['BodyText'])
            # self._elements.append(p)

            self._gen_protocol(protocol)

            # TODO delete
            # p = Paragraph('TODO paragraph after the table?', self._style_sheet['BodyText'])
            # self._elements.append(p)

        self._build()

    # -------------------
    def _gen_protocol(self, protocol):
        tbl = []
        tbl.append([
            Paragraph(f"<b>{protocol['proto_id']}</b>: {protocol['desc']}", self._style_sheet['BodyText'])
            # TODO add protocol location
            # TODO add dts?
        ])

        tbl.append(
            [
                Paragraph('<b>Step</b>'),
                Paragraph('<b>Description</b>'),
                Paragraph('<b>Pass /\nFail</b>'),
                Paragraph('<b>Actual</b>'),
                Paragraph('<b>Expected</b>'),
                Paragraph('<b>Details</b>')
            ]
        )

        stepno = 0
        for step in protocol['steps']:
            stepno += 1
            self._gen_step(tbl, stepno, step)

        self._gen_summary_table(tbl)

    # -------------------
    def _gen_step(self, tbl, stepno, step):
        # default is a passed, and empty result
        rs = ResultSummary()
        rs.passed()
        for res in step['results']:
            rs = ResultSummary()
            rs.load(res)
            if rs.result == 'FAIL':
                break

        desc = Paragraph(step['desc'], self._style_sheet['BodyText'])
        result = rs.result
        actual = rs.actual
        expected = rs.expected
        details = str(rs.location) + '\n'
        details += str(step['dts']) + '\n'
        details += 'reqid=' + str(rs.reqid)

        tbl.append([stepno, desc, result, actual, expected, details])

    # -------------------
    def _gen_summary_table(self, tbl):

        tbl_widths = [
            0.50 * inch,  # stepno
            3.20 * inch,  # desc
            0.50 * inch,  # result
            1.20 * inch,  # actual
            1.20 * inch,  # expected
            1.50 * inch,  # details
        ]

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.25 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                # top row spans all columns
                ('BACKGROUND', (0, 0), (5, 0), colors.lightblue),
                ('SPAN', (0, 0), (5, 0)),

                # 2nd row is a title row
                ('BACKGROUND', (0, 1), (5, 1), colors.lightgrey),

                # "step#" column is middle/center
                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),

                ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),

                # "pass/fail" column is middle/center
                ('VALIGN', (2, 0), (2, -1), 'MIDDLE'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),

                ('VALIGN', (3, 0), (3, -1), 'MIDDLE'),
                ('VALIGN', (4, 0), (4, -1), 'MIDDLE'),
                ('VALIGN', (5, 0), (5, -1), 'MIDDLE'),
            ]
        ))
        self._elements.append(t)

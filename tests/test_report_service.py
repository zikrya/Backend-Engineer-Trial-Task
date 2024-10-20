from django.test import TestCase
from services.report_service import ReportService

class ReportServiceTest(TestCase):

    def test_generate_json_report(self):
        report = ReportService.generate_json_report('AAPL')
        self.assertIn('total_return', report)
        self.assertIn('max_drawdown', report)
        self.assertIn('graph', report)

    def test_generate_pdf_report(self):
        pdf_report = ReportService.generate_pdf_report('AAPL')
        self.assertIsNotNone(pdf_report)
        self.assertGreater(len(pdf_report), 0)

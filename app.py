from DescriptionPdfGenerator.PdfGen import PdfGen

input = input("Please enter your topic: ")
pdf = PdfGen(input)
pdf.generate_pdf()
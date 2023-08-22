from fpdf import FPDF
# from DescriptionPdfGenerator.ImgGen import ImgGen
from DescriptionPdfGenerator.TextGen import TextGen
import warnings

warnings.filterwarnings("ignore")

class PdfGen:
    def __init__(self, input):
        textGen = TextGen()
        self.text = textGen.text_generator(input)
        # updated_text = f"Image of ({self.text['input'][0] + self.text['Origin'] + self.text['Description'] +self.text['Applications']}) without any text)"
        # imgGen = ImgGen()
        # self.image = imgGen.img_generator(updated_text)
        
    def generate_pdf(self):
        # Create a PDF instance
        pdf = FPDF()
        pdf.add_page()

        # Set font
        pdf.set_font("Times", size=12)  # Using a different font (Times)

        # Set border color and width
        border_color = (30, 30, 30)  # Darker color
        border_width = 4  # Increased width

        # Add a border around the entire page as a margin
        pdf.set_draw_color(*border_color)
        pdf.rect(border_width, border_width, 210 - 2 * border_width, 297 - 2 * border_width)

        # Add title with larger font size
        pdf.set_font("Arial", 'B', 35)  # Larger font size
        pdf.cell(0, 20, self.text["input"][0].upper() + '\n', 0, 1, 'C')


        # Calculate the image dimensions while maintaining aspect ratio
        # img_width = 140
        # img_height = img_height = (img_width / img.size[0]) * img.size[1]

        # Center the image horizontally
        # pdf.set_x((210 - img_width) / 2)

        # Add the image
        # pdf.image(self.image, x=pdf.get_x(), y=pdf.get_y(), w=img_width, h=img_height)
        # pdf.ln(img_height + 10)  # Move down after image

        # Add text with improved styling
        pdf.set_font("Times", size=15)
        pdf.set_text_color(0, 0, 128)  # Dark blue color
        pdf.multi_cell(
            0,
            8,  # Increased line height
            f"Origin:\n{self.text['Origin']}\n\nDescription:\n{self.text['Description']}\n\nApplication:\n{self.text['Applications']}",
            align="L",
        )

        # Add a separator line
        pdf.set_draw_color(150, 150, 150)
        pdf.line(20, pdf.get_y() + 10, 190, pdf.get_y() + 10)
        pdf.ln(10)

        # Add a footer
        pdf.set_font("Arial", style="I", size=10)
        pdf.set_text_color(0, 0, 0)  # Dark blue color
        pdf.cell(0, 10, "Assignment submitted by - Swapnil Sharma (swapnil.sharma.869.11@gmail.com)", 0, 0, "C")

        # Save the PDF to a file
        pdf.output(f"artifacts/PDFs/{self.text['input'][0]}.pdf")
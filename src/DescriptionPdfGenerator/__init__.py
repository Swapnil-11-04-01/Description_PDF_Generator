import os
from diffusers import DiffusionPipeline
from langchain import HuggingFaceHub
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
import torch
from fpdf import FPDF
from PIL import Image
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN



class TextGen:
    def __init__(self):
        self.repo_id = "google/flan-t5-xxl"
        self.llm = HuggingFaceHub(repo_id=self.repo_id,
                             model_kwargs={"temperature": 0.1,
                                           "min_length": 150})
        
    def text_generator(self, input):
        # Chain 1: Origin
        prompt_template_name = PromptTemplate(
            input_variables=['input'],
            template="When was the term ({input}) found? Answer in a sentance.")
        origin_chain = LLMChain(llm=self.llm,
                                prompt=prompt_template_name,
                                output_key="Origin")

        # Chain 2: Description
        prompt_template_name = PromptTemplate(
            input_variables=['input'],
            template="State the definition of {input}.")
        desc_chain = LLMChain(llm=self.llm,
                              prompt=prompt_template_name,
                              output_key="Description")

        # Chain 3: Applications
        prompt_template_items = PromptTemplate(
            input_variables=['input'],
            template="What is the main applications of {input}?")
        application_chain = LLMChain(llm=self.llm,
                                     prompt=prompt_template_items,
                                     output_key="Applications")

        chain = SequentialChain(
            chains=[origin_chain, desc_chain, application_chain],
            input_variables=['input'],
            output_variables=['Origin', 'Description', "Applications"]
            )

        response = chain({'input': input})
        return response



class ImgGen:
    def __init__(self):
        self.pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        self.pipe.to("cuda")
        
    def img_generator(self, summary):
        prompt = summary
        image = self.pipe(prompt=prompt).images[0]
        return image



class PdfGen:
    def __init__(self, input):
        textGen = TextGen()
        self.text = textGen.text_generator(input)
        updated_text = f"Image of ({self.text['input'][0] + self.text['Origin'] + self.text['Description'] +self.text['Applications']}) without any text)"
        imgGen = ImgGen()
        self.image = imgGen(updated_text)
        
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
        pdf.cell(0, 20, output[0]["input"][0].upper() + '\n', 0, 1, 'C')


        # Calculate the image dimensions while maintaining aspect ratio
        img_width = 140
        img_height = img_height = (img_width / img.size[0]) * img.size[1]

        # Center the image horizontally
        pdf.set_x((210 - img_width) / 2)

        # Add the image
        img = output[1]
        pdf.image(img, x=pdf.get_x(), y=pdf.get_y(), w=img_width, h=img_height)
        pdf.ln(img_height + 10)  # Move down after image

        # Add text with improved styling
        pdf.set_font("Times", size=15)
        pdf.set_text_color(0, 0, 128)  # Dark blue color
        pdf.multi_cell(
            0,
            8,  # Increased line height
            f"Origin:\n{output[0]['Origin']}\n\nDescription:\n{output[0]['Description']}\n\nApplication:\n{output[0]['Applications']}",
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
        pdf.output(f"{output[0]['input'][0]}.pdf")
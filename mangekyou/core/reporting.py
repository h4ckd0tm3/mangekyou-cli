import colorlog

from typing import *
from fpdf import FPDF
from logging import Logger
from mangekyou.core.config import Config
from mangekyou.beans.target import Target


class Reporting:
    config: Config
    logger: Logger

    def __init__(self, config: Config):
        self.config = config
        self.logger = colorlog.getLogger("mangekyou:reporting")
        self.logger.addHandler(self.config.handler)

    def target_to_pdf(self, target: Target, target_path: str):
        self.logger.debug("Creating PDF Report.")

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Mangekyou Report", ln=1, align="C")
        pdf.set_font_size(12)
        pdf.image(target.face, x=10, w=50)
        pdf.cell(65)
        pdf.cell(200, 20, txt=f"Name: {target.name}", ln=1)
        pdf.cell(200, 10, txt="Profiles:", ln=1)

        for profile in target.profiles:
            pdf.cell(200, 20, txt=f"{profile.url}", ln=1)

        pdf.output(f"{target_path}/report.pdf")

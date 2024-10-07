import apriltag
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image, ImageDraw
from moms_apriltag import ApriltagBoard
import os

from moms_apriltag import ApriltagBoard
import imageio

# Create AprilTag board with 5x6 tags and 0.02m spacing
board = ApriltagBoard.create(5,7,"tag25h9", 0.02)
tgt = board.board

# Save the image
filename = "apriltag_target.png"
imageio.imwrite(filename, tgt)

# Use online png to pdf 
# Or Convert PNG to PDF
# pdf_filename = "apriltag_target.pdf"
# c = canvas.Canvas(pdf_filename, pagesize=letter)
# c.drawImage(filename, 0, 0, width=8*inch, height=6*inch) # if 4,6 then 8.5*inch, 11*inch; if 5*7 then 8*inch, 6*inch
# c.save()
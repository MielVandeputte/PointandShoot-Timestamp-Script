import os
import math
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from tqdm import tqdm

scale = int(input('Logo scale (recommended value is 5): '))
text_size = int(input('Text size (recommended value is 64): '))

print('\nTimestamp adder script started...')
logo = Image.open('logo.png')

for file in tqdm(os.listdir('.')):

    if file.split('.')[-1].lower() in ['png', 'jpeg', 'jpg', 'ppm', 'gif', 'tiff', 'bmp']:

        try:
            img = Image.open(file)

            # Add timestamp
            exif = img.getexif()
            if exif is None:
                raise Exception('No exif data is found')
            
            datetime_str = exif.get(306)
            if datetime_str is None:
                raise Exception('No datetime value is found in exif data')

            datetime_form = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')

            font = ImageFont.truetype('OpenSans-SemiBold.ttf', text_size)
            img_editable = ImageDraw.Draw(img)

            text_width, text_height = img_editable.textbbox(datetime_form, font=font)

            img_editable.text((math.floor(img.size[0]/2 - text_width/2), img.size[1] - 20 - text_height), datetime_form, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, font=font)

            # Add logo
            logo = logo.resize((math.floor(img.size[0]/scale), math.floor(img.size[0]/scale*logo.size[1]/logo.size[0])))
            img.paste(logo, (math.floor(img.size[0]/2 - logo.size[0]/2), img.size[1] - logo.size[1] - 20 - text_height), logo)

            # Save modified image
            if not os.path.exists('result'):
                os.makedirs('result')

            img.save(f'result/{file}')
        
        except Exception as e:
            pass
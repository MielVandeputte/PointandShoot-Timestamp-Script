import os
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import math

print('Timestamp adder script started...\n')

logo = Image.open('logo.png')

for file in os.listdir('.'):

    if file.split('.')[-1].lower() in ['png', 'jpeg', 'jpg', 'ppm', 'gif', 'tiff', 'bmp']:

        print(f'Opening {file}:\t', end='')

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
            print(datetime_form)

            font = ImageFont.truetype('OpenSans-SemiBold.ttf')
            img_editable = ImageDraw.Draw(img)
            img_editable.text((5000,3000), datetime_form, (237, 230, 211), font=font)

            # Add logo
            logo = logo.resize((math.floor(img.size[0]/10), math.floor(img.size[0]/10*logo.size[1]/logo.size[0])))
            img.paste(logo, (math.floor(img.size[0]/2 - logo.size[0]/2), img.size[1] - logo.size[1] - 20), logo)

            # Save modified image
            if not os.path.exists('result'):
                os.makedirs('result')

            img.save(f'result/{file}')
        
        except Exception as e:
            print(e)

    
            

    
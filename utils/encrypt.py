import numpy as np
import os
from PIL import Image
import csv

def encrypt_text(username=None, password=None):
    try:
        binary_to_value = {}
        mapping_csv = './mapping.csv'
        with open(mapping_csv, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    binary_string = row[0].strip() 
                    color_value = row[1].strip()
                    binary_to_value[binary_string] = color_value         
        binary_string = f"uname={username if username else ''};pass={password if password else ''}"      
        chunk_size = 24
        binary_chunks = [binary_string[i:i + chunk_size] for i in range(0, len(binary_string), chunk_size)]
        zeros_added = 0           
        if len(binary_chunks[-1]) < chunk_size:
            padding_needed = chunk_size - len(binary_chunks[-1])  
            zeros_added = padding_needed
            binary_chunks[-1] = binary_chunks[-1].ljust(chunk_size, '0')  
        hash = len(binary_chunks)
        atthe = zeros_added
        det = f"{hash}@{atthe}"
        color_values = []
        for chunk in binary_chunks:
            if chunk in binary_to_value:
                color_values.append(binary_to_value[chunk])
            else:
                color_values.append('#808080')                    
        e_image_width = 3840
        e_image_height = 2160
        num_pixels = e_image_width * e_image_height
        num_color_values = len(binary_chunks)
        if num_color_values < num_pixels:
            img_width = min(num_color_values, 3840)
            img_height = (num_color_values + img_width - 1) // img_width

            img = Image.new('RGB', (img_width, img_height))
            pixels = []
            for color in color_values:
                rgb_color = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                pixels.append(rgb_color)

            img.putdata(pixels)
            img_filename = f'{det}.png'
            img.save(os.path.join('static/images', img_filename))
            image_url = f'http://127.0.0.1:5000/static/images/{img_filename}'
        else:
            output_folder = "http://127.0.0.1:5000/static/images/output_images"
            os.makedirs(output_folder, exist_ok=True)
            num_images = num_color_values // num_pixels + (1 if num_color_values % num_pixels > 0 else 0)
            print(f"Total images to create: {num_images}")
            for i in range(num_images):
                img = Image.new('RGB', (e_image_width, e_image_height))
                start_index = i * num_pixels
                end_index = start_index + num_pixels
                current_color_values = color_values[start_index:end_index]
                pixels = []
                for color in current_color_values:
                    rgb_color = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                    pixels.append(rgb_color)
                if len(pixels) < num_pixels:
                    pixels.extend([(128, 128, 128)] * (num_pixels - len(pixels)))
                img.putdata(pixels)
                img_filename = f'{det}_{i + 1}.png'
                img_path = os.path.join(output_folder, img_filename)
                img.save(img_path)
                image_url = f'http://127.0.0.1:5000/static/images/output_images/{img_filename}'
        return {
            'success': True,
            'Image': image_url,
            'name' : det  
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Encryption failed: {str(e)}"
        }

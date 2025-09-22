import numpy as np
import re

def extract_resolution(header_line):
    """Extrae la resolución del tipo Resolution: (600,896)"""
    match = re.search(r"Resolution:\s*\((\d+),\s*(\d+)\)", header_line)
    if not match:
        raise ValueError("No se pudo extraer la resolución de la cabecera.")
    width, height = map(int, match.groups())
    return width, height

def read_file(filename):
    is_text = filename.endswith(".ls")

    with open(filename, "rb") as f:
        header = f.readline().decode('utf-8')
        

        width, height = extract_resolution(header)
        frame_size = width * height

        
        raw_data = f.read()
                
        
        num_frames = len(raw_data) // (height * width)

        video_data = np.frombuffer(raw_data, dtype=np.uint8).reshape((num_frames,  width, height))      
    
    
    return video_data
import os

# Carpeta raíz del proyecto (donde está este config.py)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Un directorio atrás
ROOT_DIR = os.path.dirname(CURRENT_DIR)

# Ejemplo: carpeta de assets
ASSETS_DIR = os.path.join(ROOT_DIR, "Assets")
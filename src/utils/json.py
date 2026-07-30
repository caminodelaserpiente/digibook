# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Repository: https://github.com/caminodelaserpiente/DigiBook

"""
Módulo de serialización y persistencia de datos (JSON).

Permite almacenar diccionarios de Python en disco de manera segura,
generando nombres únicos basados en marcas de tiempo y garantizando
el soporte adecuado para codificación UTF-8 e indentación legible.
"""

from datetime import datetime
import json
import os

from src.utils import logger


def save_json(data: dict, filename: str, folder: str) -> str | None:
    """
    Guarda un diccionario de Python como archivo JSON estructurado en disco.

    Args:
        data (dict): Diccionario que contiene la información a persistir.
        filename (str): Nombre base asignado al archivo (sin la extensión .json).
        folder (str): Directorio o carpeta de destino donde se ubicará el archivo.

    Returns:
        str | None: La ruta completa del archivo generado en caso de éxito, o None si ocurre un fallo.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_path = os.path.join(folder, f"{filename}_{timestamp}.json")

        with open(full_path, "w", encoding="utf-8") as file_stream:
            json.dump(data, file_stream, ensure_ascii=False, indent=4)

        return full_path

    except TypeError as error:
        logger.log(
            f"Error de serialización JSON al guardar '{filename}': {str(error)}. "
            "Verifica la compatibilidad de los datos.", 
            "error"
        )
        return None
    except OSError as error:
        logger.log(
            f"Error de disco o permisos al intentar guardar '{filename}': {str(error)}", 
            "error"
        )
        return None
    except Exception as error:
        logger.log(
            f"Error crítico inesperado al procesar el archivo '{filename}': {str(error)}", 
            "error"
        )
        return None

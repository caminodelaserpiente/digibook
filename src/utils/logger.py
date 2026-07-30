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
Módulo de registro centralizado (Logging).

Configura un sistema de logging dual que emite mensajes en texto plano
hacia un archivo de salida y aplica formato condicional con colores ANSI
para la visualización en tiempo real dentro de la consola.
"""

import logging
import os
import sys

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

COLORS = {
    "WARNING": "\033[93m",      # Amarillo
    "ERROR": "\033[91m",        # Rojo
    "CRITICAL": "\033[91;1m",   # Rojo brillante/negrita
    "INFO": "\033[94m",         # Azul
    "RESET": "\033[0m",         # Restablecer valores por defecto
}


class ColoredConsoleFormatter(logging.Formatter):
    """
    Formateador personalizado que inyecta códigos de color ANSI de forma condicional
    exclusivamente para los flujos de salida en la consola del sistema.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Aplica estilos de color dinámicos basados en el nivel de severidad del registro."""
        color = COLORS.get(record.levelname, "")
        reset = COLORS["RESET"] if color else ""

        format_str = f"%(asctime)s [{color}%(levelname)s{reset}] {color}%(message)s{reset}"
        formatter = logging.Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# Inicialización del logger principal aislado para evitar colisiones con librerías externas (Playwright)
_logger = logging.getLogger("DigiBookLogger")
_logger.setLevel(logging.DEBUG)
_logger.propagate = False

if not _logger.handlers:
    # Manejador 1: Registro en archivo plano (sin secuencias ANSI, nivel INFO en adelante)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "scraper.log"), encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)

    # Manejador 2: Registro en consola con formato enriquecido.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredConsoleFormatter())

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)


def log(msg: str, level: str = "info") -> None:
    """
    Despacha un mensaje formateado de manera concurrente hacia la consola (con color).

    Args:
        msg (str): Mensaje a registrar.
        level (str): Nivel de severidad ('info', 'warning', 'error', 'debug', 'critical').
    """
    level_lower = level.lower()

    if level_lower == "error":
        _logger.error(msg)
    elif level_lower == "warning":
        _logger.warning(msg)
    elif level_lower == "debug":
        _logger.debug(msg)
    elif level_lower == "critical":
        _logger.critical(msg)
    else:
        _logger.info(msg)

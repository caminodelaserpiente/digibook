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

import argparse
import os

from src.digimonitor.scraper.maps import GMScraper
from src.digimonitor.scraper.tiktok import TKScraper
from src.digimonitor.scraper.youtube import YTScraper
from src.digimonitor.scraper.youtubes import YTSScraper
from src.utils import logger


def parse_args() -> argparse.Namespace:
    """
    Configura y procesa los argumentos de la línea de comandos.

    Returns:
        argparse.Namespace: Los argumentos analizados y validados provistos por el usuario.
    """
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        '-m', '--max-concurrent', 
        type=int, 
        default=3, 
        help='Concurrencia máxima de navegadores o hilos.'
    )
    base_parser.add_argument(
        '--headless', 
        action='store_false', 
        help='Ejecutar con interfaz gráfica visible.'
    )
    base_parser.add_argument(
        '-o', '--output-dir', 
        type=str, 
        default="out_storage", 
        help="Directorio de almacenamiento para los datos extraídos."
    )

    parser = argparse.ArgumentParser(description="DIGIBOOK: Sociology Tool for Social Media Analysts.")
    subparsers = parser.add_subparsers(dest="scraper_type", required=True, help="Elige el scraper a ejecutar")

    # YouTube
    yt_parser = subparsers.add_parser('youtube', parents=[base_parser], help="Ejecutar scraper de YouTube")
    yt_parser.add_argument('-f', '--urls-file', type=str, required=True, help='Archivo de URLs de YouTube.')
    yt_parser.add_argument(
        '-p', '--profile-path', 
        type=str, 
        required=False, 
        help='Ruta absoluta al perfil de Firefox (Opcional para YouTube).'
    )

    # YouTube Shorts
    yts_parser = subparsers.add_parser('youtube-shorts', parents=[base_parser], help="Ejecutar scraper de YouTube Shorts")
    yts_parser.add_argument('-f', '--urls-file', type=str, required=True, help='Archivo de URLs de YouTube Shorts.')
    yts_parser.add_argument(
        '-p', '--profile-path', 
        type=str, 
        required=False, 
        help='Ruta absoluta al perfil de Firefox (Opcional para YouTube Shorts).'
    )

    # Google Maps
    gm_parser = subparsers.add_parser('maps', parents=[base_parser], help="Ejecutar scraper de Google Maps")
    gm_parser.add_argument('-f', '--urls-file', type=str, required=True, help='Archivo de URLs de Maps.')
    gm_parser.add_argument(
        '-p', '--profile-path', 
        type=str, 
        required=True, 
        help='Ruta absoluta al perfil de Firefox (Requerido para Maps).'
    )

    # TikTok
    tk_parser = subparsers.add_parser('tiktok', parents=[base_parser], help="Ejecutar scraper de TikTok")
    tk_parser.add_argument('-f', '--urls-file', type=str, required=True, help='Archivo de URLs de TikTok.')
    tk_parser.add_argument(
        '-p', '--profile-path', 
        type=str, 
        required=False, 
        help='Ruta absoluta al perfil de Firefox (Opcional para TikTok).'
    )

    return parser.parse_args()


def main() -> None:
    """
    Inicializa el entorno y lanza el scraper correspondiente con base en los argumentos.
    """
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    try:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]

        if not urls:
            logger.log("El archivo de URLs está vacío. No hay objetivos que procesar.", "warning")
            return

        if args.scraper_type == 'youtube':
            logger.log(f"Iniciando extracción para YouTube. URLs en cola: {len(urls)}.", "info")
            scraper = YTScraper(urls, args.max_concurrent, args.output_dir, args.headless, args.profile_path)

        elif args.scraper_type == 'youtube-shorts':
            logger.log(f"Iniciando extracción para YouTube Shorts. URLs en cola: {len(urls)}.", "info")
            scraper = YTSScraper(urls, args.max_concurrent, args.output_dir, args.headless, args.profile_path)

        elif args.scraper_type == 'maps':
            logger.log(f"Iniciando extracción para Google Maps. URLs en cola: {len(urls)}.", "info")
            scraper = GMScraper(urls, args.max_concurrent, args.output_dir, args.headless, args.profile_path)

        elif args.scraper_type == 'tiktok':
            logger.log(f"Iniciando extracción para TikTok. URLs en cola: {len(urls)}.", "info")
            scraper = TKScraper(urls, args.max_concurrent, args.output_dir, args.headless, args.profile_path)

        scraper.run()

    except KeyboardInterrupt:
        print() 
        logger.log("Proceso interrumpido por el usuario (Ctrl+C).", "warning")
    except FileNotFoundError:
        logger.log(f"Archivo no encontrado: {args.urls_file}", "error")


if __name__ == "__main__":
    main()

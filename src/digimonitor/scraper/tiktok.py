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


import asyncio
from typing import List, Optional

from src.digimonitor.driver.browser_manager import BrowserManager
from src.utils import logger

class TKScraper:
    """
    Orquesta la extracción asincrónica de TikTok 
    utilizando un navegador controlado por Playwright.

    Attributes:
        urls (List[str]): Lista de URLs de videos a procesar.
        max_concurrent (int): Límite máximo de pestañas o contextos abiertos
                              simultáneamente mediante un semáforo asincrónico.
        output_dir (str): Directorio de destino para almacenar los archivos JSON.
        headless (bool): Define si el navegador opera sin interfaz gráfica.
        profile_path (Optional[str]): Ruta absoluta al perfil de usuario.
    """

    def __init__(
        self, 
        urls: List[str], 
        max_concurrent: int, 
        output_dir: str, 
        headless: bool,
        profile_path: Optional[str] = None
    ) -> None:
        """Inicializa los parámetros de configuración base para el scraping."""
        self.urls = urls
        self.max_concurrent = max_concurrent
        self.output_dir = output_dir
        self.headless = headless
        self.profile_path = profile_path


    async def _process_url(self, sem: asyncio.Semaphore, context, url: str, index: int) -> None:
        async with sem:
            page = context.pages[0] if index == 0 and len(context.pages) > 0 else await context.new_page()

            # =============================================================================
            # Nota:
            # Para consultas ponerse en contacto con el equipo de soporte:
            # =============================================================================

            try:
                print("OK")

            except Exception as error:
                logger.log(f"[URL {index + 1}] Error crítico en '_process_url': {str(error)}", "error")
            finally:
                if not page.is_closed():
                    await page.close()
                logger.log(f"[URL {index + 1}] Extracción y cierre finalizadas.")


    async def _run(self) -> None:
        """
        Gestiona la concurrencia inicializando el navegador y las tareas paralelas.
        """
        sem = asyncio.Semaphore(self.max_concurrent)

        async with BrowserManager(
            headless=self.headless, 
            profile_path=self.profile_path
        ) as context:

            tasks = [
                self._process_url(sem, context, url, i)
                for i, url in enumerate(self.urls)
            ]

            await asyncio.gather(*tasks)

    def run(self) -> None:
        """Punto de entrada síncrono público para disparar la ejecución asincrónica del scraper."""
        asyncio.run(self._run())

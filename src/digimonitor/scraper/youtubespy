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
Módulo de extracción automatizada para YouTube Shorts utilizando Playwright.

Este script implementa el scraper YTSScraper, diseñado para procesar múltiples
URLs en paralelo de manera concurrente, extraer metadatos
estructurados y almacenar los resultados en formato JSON.
"""


import asyncio
import random
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from src.digimonitor.driver.browser_manager import BrowserManager
from src.utils import logger
from src.utils.json import save_json

class YTSScraper:
    """
    Orquesta la extracción asincrónica de YouTube Shorts 
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


    async def _click_comments(self, page, live_index: int) -> None:
        """Localiza y despliega la sección de comentarios en la interfaz del Short."""
        try:
            target = 'button[aria-label*="comentario" i], button[aria-label*="comment" i]'
            target = page.locator(target).first
            await target.wait_for(state="visible", timeout=5000)
            await target.click()
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_click_comments' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_click_comments': {str(error)}", "error")


    async def _extract_id_channel(self, page, live_index: int) -> str | None:
        """Extrae el identificador o enlace canónico del canal del autor."""
        try:
            target = page.locator('//link[@itemprop="url"]').nth(1)
            await target.wait_for(state="attached", timeout=5000)
            return await target.get_attribute("href")
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_id_channel' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_id_channel': {str(error)}", "error")

    async def _extract_url_post(self, page, live_index: int) -> str | None:
        """Extrae la URL del post."""
        try:
            target = page.locator('//link[@itemprop="url"]').first
            await target.wait_for(state="attached", timeout=5000)
            return await target.get_attribute("href")
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_url_post' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_url_post': {str(error)}", "error")

    async def _extract_upload(self, page, live_index: int) -> str | None:
        """Extrae la fecha de publicación."""
        try:
            target = page.locator('//meta[@itemprop="datePublished"]').first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return content.strip() if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_upload' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_upload': {str(error)}", "error")

    async def _extract_thumbnail(self, page, live_index: int) -> str | None:
        """Extrae la URL de la miniatura de previsualización."""
        try:
            target = page.locator('//meta[@property="og:image"]').first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return content.strip() if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_thumbnail' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_thumbnail': {str(error)}", "error")

    async def _extract_title_post(self, page, live_index: int) -> str | None:
        """Extrae el título del video."""
        try:
            target = page.locator('//meta[@itemprop="name"]').first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return content.strip() if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_title_post' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_title_post': {str(error)}", "error")

    async def _extract_categoria_post(self, page, live_index: int) -> str | None:
        """Extrae la categoría temática asociada al contenido."""
        try:
            target = page.locator('//meta[@itemprop="genre"]').first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return content.strip() if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_categoria_post' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_categoria_post': {str(error)}", "error")

    async def _extract_likes_post(self, page, live_index: int) -> int | None:
        """Extrae el volumen numérico total de 'Me gusta' del video."""
        try:
            target = (
                '//meta[@itemprop="interactionType" and @content="https://schema.org/LikeAction"]'
                '/following-sibling::meta[@itemprop="userInteractionCount"]'
            )
            target = page.locator(target).first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return int(content) if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_likes_post' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_likes_post': {str(error)}", "error")

    async def _extract_count_comments(self, page, live_index: int) -> int | None:
        """Extrae la cantidad total de comentarios."""
        try:
            target = 'button[aria-label*="comentario" i], button[aria-label*="comment" i]'
            target = page.locator(target).first
            await target.wait_for(state="attached", timeout=5000)

            content = await target.get_attribute("aria-label")
            if content:
                content = "".join(filter(str.isdigit, content))
                if content:
                    return int(content)

            target = target.locator('xpath=following-sibling::div//span').first
            if await target.count() > 0:
                content = await target.inner_text()
                if content:
                    content = "".join(filter(str.isdigit, content))
                    return int(content) if content else None

        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_count_comments' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_count_comments': {str(error)}", "error")

    async def _extract_count_views(self, page, live_index: int) -> int | None:
        """Extrae el conteo total de visualizaciones del video."""
        try:
            target = (
                '//meta[@itemprop="interactionType" and @content="https://schema.org/WatchAction"]'
                '/following-sibling::meta[@itemprop="userInteractionCount"]'
            )
            target = page.locator(target).first
            await target.wait_for(state="attached", timeout=5000)
            content = await target.get_attribute("content")
            return int(content) if content else None
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_count_views' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_count_views': {str(error)}", "error")

    async def _extract_comments_emojis(self, page, live_index: int) -> list[str]:
        """Extrae el texto de los comentarios."""
        target = '//yt-attributed-string[@id="content-text"]'
        results = []
        try:
            target = page.locator(target)
            await target.first.wait_for(state="attached", timeout=3000)
            target = await target.all()
            for element in target:
                content = await element.inner_html()
                soup = BeautifulSoup(content, "html.parser")
                content = ""
                for elem in soup.recursiveChildGenerator():
                    if getattr(elem, "name", None) == "img":
                        alt = elem.get("alt")
                        if alt:
                            content += alt
                    elif isinstance(elem, str):
                        content += elem
                results.append(content.strip())
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_comments_emojis' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_comments_emojis': {str(error)}", "error")
        return results

    async def _extract_n_likes(self, page, live_index: int) -> list[str]:
        """Extrae likes correspondientes a cada comentario."""
        target = '//span[@id="vote-count-middle"]'
        results = []
        try:
            target = page.locator(target)
            await target.first.wait_for(state="attached", timeout=3000)
            target = await target.all()
            for element in target:
                content = await element.inner_text()
                results.append(content.strip() if content else "")
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_n_likes' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_n_likes': {str(error)}", "error")
        return results

    async def _extract_dates(self, page, live_index: int) -> list[str]:
        """Extrae la temporalidad de la publicación del comentarios."""
        target = '//span[@id="published-time-text"]/a'
        results = []
        try:
            target = page.locator(target)
            await target.first.wait_for(state="attached", timeout=3000)
            target = await target.all()
            for element in target:
                content = await element.inner_text()
                results.append(content.strip() if content else "")
        except PlaywrightTimeoutError:
            logger.log(f"[URL {live_index + 1}] Timeout: Elemento '_extract_dates' no encontrado.", "warning")
        except Exception as error:
            logger.log(f"[URL {live_index + 1}] Error en '_extract_dates': {str(error)}", "error")
        return results


    async def _process_url(self, sem: asyncio.Semaphore, context, url: str, index: int) -> None:
        async with sem:
            page = context.pages[0] if index == 0 and len(context.pages) > 0 else await context.new_page()

            try:
                await page.goto(url, wait_until="commit")
                logger.log(f"[URL {index + 1}] Abriendo URL: {url}")

                target = '//div[@class="ytReelPlayerOverlayViewModelActionsContainer"]'
                await page.wait_for_selector(target)
                target = '//div[@class="ytReelPlayerOverlayViewModelMetadataContainerMetapanel"]'
                await page.wait_for_selector(target)

                video_data = {
                    "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "original_url": url,
                }

                video_data["channel_id"] = await self._extract_id_channel(page, index)
                video_data["post_url"] = await self._extract_url_post(page, index)
                video_data["post_upload_date"] = await self._extract_upload(page, index)
                video_data["post_thumbnail"] = await self._extract_thumbnail(page, index)
                video_data["post_title"] = await self._extract_title_post(page, index)
                video_data["post_category"] = await self._extract_categoria_post(page, index)
                video_data["post_likes_count"] = await self._extract_likes_post(page, index)
                video_data["post_comments_count"] = await self._extract_count_comments(page, index)
                video_data["post_views_count"] = await self._extract_count_views(page, index)

                await self._click_comments(page, index)

                same_size = False
                for attempt in range(3):
                    video_data["comentarios"] = await self._extract_comments_emojis(page, index)
                    video_data["likes"] = await self._extract_n_likes(page, index)
                    video_data["dates"] = await self._extract_dates(page, index)

                    # Verificación rápida de tamaños
                    if len(video_data["comentarios"]) == len(video_data["likes"]) == len(video_data["dates"]):
                        same_size = True
                        break
                    logger.log(f"[URL {index + 1}] Intento {attempt + 1}: Inconsistencia en listas de comentarios.")
                    if attempt < 2:
                        await asyncio.sleep(1)

                video_data["same_size"] = same_size

                file_path = save_json(video_data, filename=f"youtube-shorts_{index + 1}", folder=self.output_dir)
                if file_path:
                    logger.log(f"[URL {index + 1}] Datos guardados en: {file_path}")
                else:
                    logger.log(f"[URL {index + 1}] Fallo al guardar en disco.", "error")

            except PlaywrightTimeoutError:
                logger.log(f"[URL {index + 1}] Timeout: Fallo al cargar contenedor principal.", "error")
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

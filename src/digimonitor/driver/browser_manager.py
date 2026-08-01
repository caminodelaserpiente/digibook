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

from typing import Optional, Any
from playwright.async_api import (
    async_playwright,
    Playwright,
    Browser,
    BrowserContext
)

class BrowserManager:
    """
    Gestiona el ciclo de vida de un navegador Firefox de forma asíncrona.

    Actúa como un gestor de contexto asíncrono (`async with`) para inicializar,
    configurar y cerrar un entorno de navegación de Playwright.

    Attributes:
        headless (bool): Define si el navegador opera en modo oculto (sin interfaz).
        profile_path (Optional[str]): Ruta absoluta al directorio del perfil de Firefox.
    """

    def __init__(self, headless: bool, profile_path: Optional[str] = None) -> None:
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.headless: bool = headless
        self.profile_path: Optional[str] = profile_path

    async def __aenter__(self) -> BrowserContext:
        """
        Inicializa Playwright y lanza la instancia del navegador o contexto.

        Returns:
            BrowserContext: El contexto de navegación configurado y listo para operar.
        """
        self.playwright = await async_playwright().start()

        firefox_prefs = {
            "media.autoplay.default": 5,                      # Bloquea audio y video
            "media.autoplay.blocking_policy": 2,              # Política estricta
            "media.autoplay.allow-extension-background-pages": False,
            "media.autoplay.block-event.enabled": True        # Fuerza el bloqueo a nivel evento
        }

        if self.profile_path:
            self.context = await self.playwright.firefox.launch_persistent_context(
                user_data_dir=self.profile_path,
                headless=self.headless,
                firefox_user_prefs=firefox_prefs
            )
        else:
            self.browser = await self.playwright.firefox.launch(
                headless=self.headless,
                firefox_user_prefs=firefox_prefs
            )
            self.context = await self.browser.new_context()

        return self.context

    async def __aexit__(
        self, 
        exc_type: Optional[Any], 
        exc_val: Optional[Any], 
        exc_tb: Optional[Any]
    ) -> None:
        """
        Garantiza el cierre limpio y ordenado de los recursos de navegación.
        """
        if self.context:
            await self.context.close()

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

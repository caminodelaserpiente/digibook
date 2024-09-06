# Digimonitor is part of the DIGIBOOK collection.
# DIGIBOOK Copyright (C) 2024 Daniel Alcalá.
# Contact: daniel.alcala.py@gmail.com
# Public Copyright Registration Number (INDAUTOR): 03-2024-080111090400-14

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License and the GNU Affero General 
# Public Licenseas published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License and the GNU Affero General Public License
# for more details.

# You should have received a copy of the GNU General Public License and the GNU
# Affero General Public License along with this program. If not, see 
# <https://www.gnu.org/licenses/>.


import re

def DetectPlatform(url: str) -> str:
    """
    Detects whether the provided URL belongs to YouTube or is invalid.

    This function uses regular expressions to identify if the given URL matches
    the patterns for YouTube If the URL matches none of these patterns, it is
    considered invalid.

    Args:
        url (str): The URL to analyze.

    Returns:
        str: The detected platform. It returns 'youtube' if the URL matches YouTube,
            and 'INVALIDURL' if it matches neither.
    """
    youtube_pattern = re.compile(r'https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+')

    if youtube_pattern.match(url):
        return 'youtube'
    else:
        return 'INVALIDURL'

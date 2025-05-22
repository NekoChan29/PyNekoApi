import os
from typing import Any, Dict, Optional, Union

import aiofiles
from io import BytesIO
from pynekoapi.tools import AsyncRequest


class AsyncNekoApi:

    def __init__(self, timeout: Optional[int] = None) -> None:
        """
        Initializes the AsyncNekoApi class.

        Args:
            timeout (Optional[int]): The timeout in seconds for HTTP requests. Defaults to None.
        """
        self.fetch = AsyncRequest(timeout)
        self.base_url = "https://api.rizkiofficial.com/v1/"

    async def get_bin(self, key: str) -> Dict[Any, Any]:
        """
        Retrieves a bin from the NekoBin API based on the given key.

        Args:
            key (str): The key of the bin to retrieve.

        Returns:
            Dict[Any, Any]: A dictionary containing the bin data.
        """
        result = await self.fetch._get(self.base_url + f"nekobin/get?key={key}")
        return result

    async def save_bin(self, content: str) -> Dict[Any, Any]:
        """
        Saves a bin to the NekoBin API.

        Args:
            content (str): The content to save.

        Returns:
            Dict[Any, Any]: A dictionary containing the result of the save operation.
        """
        result = await self.fetch._post(
            self.base_url + f"nekobin/save",
            json={"content": content},
        )
        return result

    async def register_date(
        self, user_id: int, timezone: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Registers a date for a user with the given ID.

        Args:
            user_id (int): The ID of the user to register.
            timezone (Optional[str]): The timezone to use. Defaults to None -> 'UTC'.

        Returns:
            Dict[Any, Any]: A dictionary containing the result of the registration.
        """
        url = self.base_url + f"register_date?user_id={user_id}"
        if timezone is not None:
            url += f"&tz={timezone}"
        result = await self.fetch._post(url)
        return result

    async def transcribe(self, file: Union[str, BytesIO]):
        url = self.base_url + "transcribe"
        if isinstance(file, BytesIO):
            files = {"file": (file.name, file)}
            result = await self.fetch._post(url, files=files)
        else:
            async with aiofiles.open(file, "rb") as f:
                file_name = os.path.basename(file)
                files = {"file": (file_name, await f.read())}
                result = await self.fetch._post(url, files=files)

        return result

    async def nekograph(self, file: Union[str, BytesIO]):
        url = self.base_url + "upload"
        if isinstance(file, BytesIO):
            files = {"file": (file.name, file)}
            result = await self.fetch._post(url, files=files)
        else:
            async with aiofiles.open(file, "rb") as f:
                file_name = os.path.basename(file)
                files = {"file": (file_name, await f.read())}
                result = await self.fetch._post(url, files=files)

        return result

    async def youtube_dl(
        self,
        yt_url: str,
        media_type: str = "video",
        quality: Union[int, str] = "720p",
    ):
        url = self.base_url + "youtube/download"
        payload = {
            "url": yt_url,
            "type": media_type,
            "quality": quality,
        }
        resp = await self.fetch.post(url, json=payload)
        if resp.status_code != 200:
            return {"ok": False, "error": "Failed download"}

        title = resp.headers.get("X-Video-Title", "Unknown")
        thumbnail = resp.headers.get("X-Video-Thumbnail", "")
        duration = resp.headers.get("X-Video-Duration", 0)
        artist = resp.headers.get("X-Video-Artist", "")

        output = "output.mp4" if media_type == "video" else "output.mp3"
        async with aiofiles.open(output, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=1024):
                if chunk:
                    await f.write(chunk)

        return {
            "ok": True,
            "file": output,
            "artist": artist,
            "title": title,
            "thumbnail": thumbnail,
            "duration": int(duration),
        }

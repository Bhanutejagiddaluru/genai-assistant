import asyncio
from typing import AsyncGenerator

async def stream_tokens(text: str, delay: float = 0.02) -> AsyncGenerator[str, None]:
    for i in range(0, len(text), 6):
        await asyncio.sleep(delay)
        yield text[i:i+6]

import aiohttp
import asyncio
import json
import base64
from loguru import logger
from typing import Optional
from src.boson_multimodal.data_types import ChatMLSample, Message, AudioContent

MODEL_SERVER_URL = "http://localhost:8001"

class ModelClient:
    def __init__(self, base_url: str = MODEL_SERVER_URL):
        self.base_url = base_url
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    def serialize_chat_template(self, chat_template: ChatMLSample) -> str:
        """Serialize ChatMLSample to JSON string for HTTP transport"""
        def serialize_message(msg: Message):
            if isinstance(msg.content, str):
                content = msg.content
            elif isinstance(msg.content, list):
                # Handle AudioContent objects
                content = []
                for item in msg.content:
                    if isinstance(item, AudioContent):
                        content.append({
                            "type": "audio",
                            "raw_audio": item.raw_audio,
                            "audio_url": item.audio_url
                        })
                    else:
                        content.append(item)
            else:
                content = str(msg.content)
            
            return {
                "role": msg.role,
                "content": content
            }
        
        serialized_messages = [serialize_message(m) for m in chat_template.messages]
        return json.dumps(serialized_messages)
    
    async def synthesize_speech(self, chat_template: ChatMLSample, request_id: str) -> bytes:
        """Synthesize speech using the model server"""
        try:
            session = await self.get_session()
            
            # Serialize the chat template
            serialized_template = self.serialize_chat_template(chat_template)
            
            async with session.post(
                f"{self.base_url}/synthesize",
                json={
                    "chat_template": serialized_template,
                    "request_id": request_id
                }
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # Decode base64 audio bytes
                    audio_b64 = result["audio_bytes"]
                    return base64.b64decode(audio_b64)
                else:
                    error_text = await response.text()
                    raise Exception(f"Model server error: {error_text}")
        except Exception as e:
            logger.error(f"Failed to synthesize speech: {e}")
            raise
    
    async def transcribe_audio(self, audio_base64: str, request_id: str, model_size: str = "small") -> str:
        """Transcribe audio using the model server"""
        try:
            session = await self.get_session()
            async with session.post(
                f"{self.base_url}/transcribe",
                json={
                    "audio_base64": audio_base64,
                    "request_id": request_id,
                    "model_size": model_size
                }
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["text"]
                else:
                    error_text = await response.text()
                    raise Exception(f"Model server error: {error_text}")
        except Exception as e:
            logger.error(f"Failed to transcribe audio: {e}")
            raise

# Global client instance
model_client = ModelClient()
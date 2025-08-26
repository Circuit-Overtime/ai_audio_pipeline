from src.templates import create_speaker_chat
from src.model_client import model_client
from src.systemInstruction import generate_higgs_system_instruction
from src.intent import getIntentType
from src.utility import encode_audio_base64, validate_and_decode_base64_audio, save_temp_audio
from src.voiceMap import VOICE_BASE64_MAP
import asyncio
from typing import Optional

async def generate_tts(text: str, requestID: str, system: Optional[str] = None, clone_text: Optional[str] = None, voice: Optional[str] = "alloy") -> bytes:
    if (voice):
        with open(voice, "r") as f:
            audio_data = f.read()
            if(validate_and_decode_base64_audio(audio_data)):
                clone_path = voice
    else:
        load_audio_path = VOICE_BASE64_MAP.get("alloy")
        base64 = encode_audio_base64(load_audio_path)    
        clone_path = save_temp_audio(base64, requestID, "clone")

    result = await getIntentType(text, system)
    type = result.get("intent")
    content = result.get("content")
    print(type)
    if type not in ["DIRECT", 'REPLY']:
        type = "DIRECT"
        
    if type == "DIRECT":
        if system is None:
            system = await generate_higgs_system_instruction(text)
        else:
            system = f"""
            "You are a voice synthesis engine. Speak the user's text exactly and only as written. Do not add extra words, introductions, or confirmations.\n"
            "Apply the emotions as written in the user prompt.\n"
            "Generate audio following instruction.\n"
            "<|scene_desc_start|>\n"
                {system}\n
            "<|scene_desc_end|>"
            """
        print(f"The formatted system instruction is:- {system}")
        prepareChatTemplate = create_speaker_chat(
            text=content,
            requestID=requestID,
            system=system,
            clone_audio_path=clone_path,
            clone_audio_transcript=clone_text
        )
        # Use model client instead of direct model access
        audio_bytes = await model_client.synthesize_speech(prepareChatTemplate, requestID)
        return audio_bytes
    elif type == "REPLY":
        if system is None:
            system = await generate_higgs_system_instruction(text)
        else: 
            system = f"""
            "You are a voice synthesis engine. Speak the user's text exactly and only as written. Do not add extra words, introductions, or confirmations.\n"
            "Apply the emotions as written in the user prompt.\n"
            "Generate audio following instruction.\n"
            "<|scene_desc_start|>\n"
                {system}\n
            "<|scene_desc_end|>"
            """
        print(f"The formatted system instruction is:- {system}")
        prepareChatTemplate = create_speaker_chat(
            text=content,
            requestID=requestID,
            system=system,
            clone_audio_path=clone_path,
            clone_audio_transcript=clone_text
        )
        print(f"The prepared chat template is {prepareChatTemplate}")
        # Use model client instead of direct model access
        audio_bytes = await model_client.synthesize_speech(prepareChatTemplate, requestID)
        return audio_bytes

if __name__ == "__main__":
    async def main():
        text = "Such a beautiful day to start with!! What's on your mind?"
        requestID = "request123"
        system = None
        voice = "alloy"
        clone_path = None  
        clone_text = None
        synthesis_audio = None  
        
        audio_bytes = await generate_tts(text, requestID, system, clone_path, clone_text, voice)
        with open("output_reply.wav", "wb") as f:
            f.write(audio_bytes)
        print("Audio saved as output_reply.wav")
    asyncio.run(main())
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_tts",
            "description": "Executes the Text-to-Speech pipeline to convert text input to audio output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to be converted to speech."
                    },
                    "requestID": {
                        "type": "string",
                        "description": "Unique identifier for the request."
                    },
                    "system": {
                        "type": "string",
                        "description": "Optional system instruction or scene description for speech synthesis."
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use: predefined voice name (alloy, ballad, coral, etc.) OR direct path to .wav file (5-8 seconds). Defaults to alloy if not found.",
                        "default": "alloy"
                    }
                },
                "required": ["text", "requestID"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_ttt",
            "description": "Executes the Text-to-Text pipeline to generate text responses from text input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The input text prompt."
                    },
                    "requestID": {
                        "type": "string",
                        "description": "Unique identifier for the request."
                    },
                    "system": {
                        "type": "string",
                        "description": "Optional system instruction for text generation."
                    }
                },
                "required": ["text", "requestID"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_sts",
            "description": "Executes the Speech-to-Speech pipeline to convert speech input to speech output with optional voice cloning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The prompt or instruction for the speech processing."
                    },
                    "synthesis_audio_path": {
                        "type": "string",
                        "description": "Path to the input speech audio file (base64)."
                    },
                    "requestID": {
                        "type": "string",
                        "description": "Unique identifier for the request."
                    },
                    "system": {
                        "type": "string",
                        "description": "Optional system instruction for speech processing."
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use: predefined voice name (alloy, ballad, coral, etc.) OR direct path to .wav file (5-8 seconds). Defaults to alloy if not found.",
                        "default": "alloy"
                    }
                },
                "required": ["synthesis_audio_path", "requestID"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_stt",
            "description": "Executes the Speech-to-Text pipeline to convert speech input to text output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Prompt tor instruction that is to be done!"
                    },
                    "synthesis_audio_path": {
                        "type": "string",
                        "description": "Path to the input speech audio file (base64)."
                    },
                    "requestID": {
                        "type": "string",
                        "description": "Unique identifier for the request."
                    },
                    "system": {
                        "type": "string",
                        "description": "Optional system instruction for speech processing."
                    }
                },
                "required": ["synthesis_audio_path", "requestID"]
            }
        }
    }
]
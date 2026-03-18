"""
OpenClaw mlx-audio TTS Server

HTTP server wrapping mlx-audio TTS functionality.
Provides OpenAI-compatible /v1/audio/speech endpoint.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Import mlx-audio
try:
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
except ImportError as e:
    print(f"Error: mlx-audio not installed. Run: pip install mlx-audio")
    print(f"Details: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mlx-tts-server")

# FastAPI app
app = FastAPI(
    title="OpenClaw mlx-audio TTS Server",
    description="Text-to-Speech server using mlx-audio",
    version="0.1.0"
)

# Global model instance
model = None
model_name: Optional[str] = None
lang_code: Optional[str] = None


class SpeechRequest(BaseModel):
    """OpenAI-compatible speech request"""
    input: str
    model: Optional[str] = None
    voice: Optional[str] = None
    response_format: Optional[str] = "mp3"
    speed: Optional[float] = 1.0
    language: Optional[str] = None


class ModelInfo(BaseModel):
    """Model information"""
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "mlx-audio"


class ModelsResponse(BaseModel):
    """Models list response"""
    object: str = "list"
    data: list[ModelInfo]


@app.on_event("startup")
async def startup_event():
    """Load TTS model on startup"""
    global model, model_name, lang_code
    
    logger.info(f"Loading TTS model: {model_name}")
    try:
        model = load_model(model_name)
        logger.info(f"Model loaded successfully: {model_name}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": model_name,
        "ready": model is not None
    }


@app.get("/v1/models", response_model=ModelsResponse)
async def list_models():
    """List available models"""
    return ModelsResponse(
        data=[ModelInfo(id=model_name or "unknown")]
    )


@app.post("/v1/audio/speech")
async def generate_speech(request: SpeechRequest):
    """
    Generate speech from text.
    
    Returns MP3 audio file.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Generating speech for text: {request.input[:50]}...")
        
        # Use voice from request or default
        voice = request.voice or "af_heart"
        
        # Use language from request or global config
        language = request.language or lang_code or "a"
        
        # Generate output path
        output_dir = Path("/tmp/mlx-tts")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"speech_{os.getpid()}.mp3"
        
        # Generate audio using mlx-audio
        result = generate_audio(
            model=model,
            text=request.input,
            voice=voice,
            speed=request.speed,
            lang_code=language,
            output_path=str(output_path),
        )
        
        logger.info(f"Speech generated: {output_path}")
        
        # Return audio file
        return FileResponse(
            path=str(output_path),
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
        
    except Exception as e:
        logger.error(f"Speech generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/tts/status")
async def tts_status():
    """Get TTS server status"""
    return {
        "status": "ready" if model is not None else "loading",
        "model": model_name,
        "language": lang_code,
        "uptime": "N/A"  # Could track this
    }


def main():
    """Main entry point"""
    global model_name, lang_code
    
    parser = argparse.ArgumentParser(description="OpenClaw mlx-audio TTS Server")
    parser.add_argument(
        "--model",
        type=str,
        default="mlx-community/Kokoro-82M-bf16",
        help="TTS model to use"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=19280,
        help="Server port"
    )
    parser.add_argument(
        "--lang-code",
        type=str,
        default="a",
        help="Default language code (a=en-US, b=en-GB, z=zh, j=ja, etc.)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host"
    )
    
    args = parser.parse_args()
    
    model_name = args.model
    lang_code = args.lang_code
    
    logger.info(f"Starting TTS server on {args.host}:{args.port}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Language: {lang_code}")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()

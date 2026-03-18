"""
OpenClaw mlx-audio STT Server

HTTP server wrapping mlx-audio STT (Whisper) functionality.
Provides OpenAI-compatible /v1/audio/transcriptions endpoint.
"""

import argparse
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Import mlx-audio
try:
    from mlx_audio.stt.utils import load
    from mlx_audio.stt.generate import generate_transcription
except ImportError as e:
    print(f"Error: mlx-audio not installed. Run: pip install mlx-audio")
    print(f"Details: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mlx-stt-server")

# FastAPI app
app = FastAPI(
    title="OpenClaw mlx-audio STT Server",
    description="Speech-to-Text server using mlx-audio Whisper",
    version="0.1.0"
)

# Global model instance
model = None
model_name: Optional[str] = None
language: Optional[str] = None


class TranscriptionResponse(BaseModel):
    """Transcription response"""
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None
    segments: Optional[List[dict]] = None


class TranslationResponse(BaseModel):
    """Translation response (Whisper translate task)"""
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None


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


class VerboseTranscriptionResponse(BaseModel):
    """Verbose transcription with segments"""
    text: str
    segments: List[dict]
    language: str


@app.on_event("startup")
async def startup_event():
    """Load STT model on startup"""
    global model, model_name, language
    
    logger.info(f"Loading STT model: {model_name}")
    try:
        model = load(model_name)
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


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    model: Optional[str] = Form(None, description="Model to use"),
    language: Optional[str] = Form(None, description="Language code"),
    prompt: Optional[str] = Form(None, description="Context prompt"),
    response_format: Optional[str] = Form("json", description="Response format"),
    temperature: Optional[float] = Form(0.0, description="Sampling temperature"),
    timestamp_granularities: Optional[List[str]] = Form(None, description="Timestamp granularities")
):
    """
    Transcribe audio to text.
    
    Accepts audio file (mp3, wav, m4a, flac, etc.)
    Returns transcription text.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info(f"Transcribing audio: {file.filename} ({len(content)} bytes)")
        
        # Use language from request or global config
        lang = language or globals()["language"]
        
        # Transcribe using mlx-audio
        result = generate_transcription(
            model=model,
            audio=tmp_path,
            language=lang,
            task="transcribe",
            temperature=temperature,
        )
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"Failed to clean up temp file: {e}")
        
        logger.info(f"Transcription complete: {result.text[:50]}...")
        
        # Return based on response_format
        if response_format == "json":
            return TranscriptionResponse(
                text=result.text,
                language=getattr(result, 'language', lang),
                duration=getattr(result, 'duration', None),
                segments=getattr(result, 'segments', None)
            )
        elif response_format == "verbose_json":
            return VerboseTranscriptionResponse(
                text=result.text,
                segments=getattr(result, 'segments', []),
                language=getattr(result, 'language', lang)
            )
        else:
            # Plain text
            return JSONResponse(
                content={"text": result.text},
                media_type="text/plain"
            )
        
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        # Clean up temp file on error
        try:
            os.unlink(tmp_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/audio/translations")
async def translate_audio(
    file: UploadFile = File(..., description="Audio file to translate"),
    model: Optional[str] = Form(None, description="Model to use"),
    prompt: Optional[str] = Form(None, description="Context prompt"),
    response_format: Optional[str] = Form("json", description="Response format"),
    temperature: Optional[float] = Form(0.0, description="Sampling temperature")
):
    """
    Translate audio to English text.
    
    Accepts audio file, returns English translation.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info(f"Translating audio: {file.filename} ({len(content)} bytes)")
        
        # Translate using mlx-audio (Whisper translate task)
        result = generate_transcription(
            model=model,
            audio=tmp_path,
            task="translate",
            temperature=temperature,
        )
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"Failed to clean up temp file: {e}")
        
        logger.info(f"Translation complete: {result.text[:50]}...")
        
        return TranslationResponse(
            text=result.text,
            language="en",  # Translation always returns English
            duration=getattr(result, 'duration', None)
        )
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        try:
            os.unlink(tmp_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/stt/status")
async def stt_status():
    """Get STT server status"""
    return {
        "status": "ready" if model is not None else "loading",
        "model": model_name,
        "language": language,
        "uptime": "N/A"
    }


def main():
    """Main entry point"""
    global model_name, language
    
    parser = argparse.ArgumentParser(description="OpenClaw mlx-audio STT Server")
    parser.add_argument(
        "--model",
        type=str,
        default="mlx-community/whisper-large-v3-turbo-asr-fp16",
        help="STT model to use"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=19290,
        help="Server port"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="zh",
        help="Default language code (zh, en, ja, ko, etc.)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host"
    )
    
    args = parser.parse_args()
    
    model_name = args.model
    language = args.language
    
    logger.info(f"Starting STT server on {args.host}:{args.port}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Language: {language}")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()

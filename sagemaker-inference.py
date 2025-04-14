import os
import json5  
import torch
from TTS.api import TTS
from io import BytesIO
import soundfile as sf

MODEL_FILE_NAME = 'model_file.pth'
CONFIG_FILE_NAME = 'config.json' 

def model_fn(model_dir):
    model_path = os.path.join(model_dir, MODEL_FILE_NAME)
    config_path = os.path.join(model_dir, CONFIG_FILE_NAME)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json5.load(f)
    tts = TTS(model_path=model_path, config_path=config_path)
    if not hasattr(tts, "config") or tts.config is None:
        tts.config = config
    if hasattr(tts.__class__, "is_multi_lingual"):
        try:
            delattr(tts.__class__, "is_multi_lingual")
        except Exception:
            pass
    try:
        tts.is_multi_lingual = tts.config.get("model_params", {}).get("is_multi_lingual", False)
    except Exception:
        tts.is_multi_lingual = False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tts.to(device)
    tts.device = device  
    return tts

def input_fn(request_body, request_content_type):
    if request_content_type == 'text/plain':
        return request_body.decode('utf-8')
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    outputs = model.tts(input_data)
    waveform = outputs[0] if isinstance(outputs, tuple) else outputs
    if isinstance(waveform, torch.Tensor):
        waveform = waveform.detach().cpu().numpy()
    sample_rate = model.config.audio["sample_rate"]
    return waveform, sample_rate

def output_fn(prediction):
    waveform, sample_rate = prediction
    buffer = BytesIO()
    sf.write(buffer, waveform, sample_rate, format="WAV")
    buffer.seek(0)
    return buffer.read(), "audio/wav"

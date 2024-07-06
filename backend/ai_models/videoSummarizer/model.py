import os
from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration, BitsAndBytesConfig
from transformers.utils import quantization_config
import torch

model_dir = os.path.dirname(os.path.realpath(__file__)) + "/llava-next/"

BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

class Model:
    """
    Model class to load the model and processor
    """
    def __init__(self) -> None:
        pass
  
    def load_model():
        model = LlavaNextVideoForConditionalGeneration.from_pretrained(
            model_dir,
            low_cpu_mem_usage=True,
            torch_dtype=torch.bfloat16
        )
        return model

    def load_processor():
        processor = LlavaNextVideoProcessor.from_pretrained(model_dir)
        return processor

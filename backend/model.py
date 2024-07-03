import os
from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration, BitsAndBytesConfig

model_dir = os.path.dirname(os.path.realpath(__file__)) + "/llava-next/"

class Model:
    """
    Model class to load the model and processor
    """
    def __init__(self) -> None:
        pass
  
    def load_model():
        model = LlavaNextVideoForConditionalGeneration.from_pretrained(model_dir)
        return model

    def load_processor():
        processor = LlavaNextVideoProcessor.from_pretrained(model_dir)
        return processor
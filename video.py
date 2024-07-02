#dependencies: pip install pyktok beautifulsoup4 browser-cookie3 numpy==1.26.4 pandas requests selenium streamlit transformers av accelerate bitsandbytes protobuf sentencepiece 
import pyktok as pyk
import av
import torch
from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration
import numpy as np
import os

link = 'https://www.tiktok.com/@thejianhaotan/video/7359164697343462677?is_from_webapp=1&sender_device=pc'

def get_video(videoLink):
    pyk.specify_browser('firefox')
    pyk.save_tiktok(videoLink, True, 'data.csv')
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".mp4"):
            return filename
    return None


def read_video_pyav(container, indices):
    '''
    Decode the video with PyAV decoder.
    Args:
        container (`av.container.input.InputContainer`): PyAV container.
        indices (`List[int]`): List of frame indices to decode.
    Returns:
        result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
    '''
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])


# video intepretation
def explain_video(videoPath):
    model_id = "llava-hf/LLaVA-NeXT-Video-7B-hf"

    model = LlavaNextVideoForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True, 
    ).to(0)

    processor = LlavaNextVideoProcessor.from_pretrained(model_id)

    # define a chat histiry and use `apply_chat_template` to get correctly formatted prompt
    # Each value in "content" has to be a list of dicts with types ("text", "image", "video") 
    conversation = [
        {

            "role": "user",
            "content": [
                {"type": "text", "text": "Explain this video in detail"},
                {"type": "video"},
                ],
        },
    ]

    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

    container = av.open(videoPath)

    # sample uniformly 8 frames from the video, can sample more for longer videos
    total_frames = container.streams.video[0].frames
    indices = np.arange(0, total_frames, total_frames / 8).astype(int)
    clip = read_video_pyav(container, indices)
    inputs_video = processor(text=prompt, videos=clip, padding=True, return_tensors="pt").to(model.device)

    output = model.generate(**inputs_video, max_new_tokens=100, do_sample=False)
    return processor.decode(output[0][2:], skip_special_tokens=True)

if __name__ == "__main__":
    path_to_video = get_video(link)
    summary = explain_video(path_to_video)
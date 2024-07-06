import os
import pyktok as pyk
import av
import torch
import numpy as np
from .model import Model

class VideoSummary:
    def __init__(self):
        self.model = Model.load_model()
        self.processor = Model.load_processor()

    def get_video(self, videoLink):
        pyk.save_tiktok(videoLink, True, 'data.csv')
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".mp4"):
                return filename
        return None

    def read_video_pyav(self, container, indices):
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

    def explain_video(self, videoPath):
        
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Summarize the contents of this video very briefly while including any text shown in the video in less than a 100 tokens"},
                    {"type": "video"},
                ],
            }
        ]
        prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)

        container = av.open(videoPath)
        framesSampled = 64
        total_frames = container.streams.video[0].frames
        indices = np.arange(0, total_frames, total_frames / framesSampled).astype(int)
        clip = self.read_video_pyav(container, indices)


        inputs_video = self.processor(text=prompt, videos=clip, padding=True, return_tensors="pt").to(self.model.device)

        output = self.model.generate(**inputs_video, max_new_tokens=100, do_sample=False)

        unprocessed_text = self.processor.decode(output[0], skip_special_tokens=True)

        # Close the container
        container.close()

        # Return text after "ASSISTANT:"
        return unprocessed_text.split("ASSISTANT:")[1].strip()

    def clean_up(self, filename):
        os.remove(filename)
        os.remove('data.csv')

    def get_video_summary(self, link):
        filename = self.get_video(link)
        summary = self.explain_video(filename)
        self.clean_up(filename)
        return {"summary": summary}
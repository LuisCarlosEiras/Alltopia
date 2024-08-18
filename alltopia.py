import streamlit as st
import av
from streamlit_webrtc import webrtc_streamer

# Create a camera input stream
streamer = webrtc_streamer(key="camera")

# Get the video frame from the stream
frame = streamer.video_frame

# Display the video frame
st.image(frame)

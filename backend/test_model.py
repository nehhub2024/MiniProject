import cv2
import numpy as np

from watermark_engine.embed_dwt_dct_svd import EmbedDwtDctSvd

# Load test image
image = cv2.imread("test.jpg")

if image is None:
    raise Exception("test.jpg not found")

# Example watermark bits
watermark_bits = [1,0,1,1,0,0,1,0]

# Create embedder
embedder = EmbedDwtDctSvd(watermark_bits)

# Embed watermark
watermarked = embedder.encode(image)

# Save output
cv2.imwrite("watermarked.jpg", watermarked)

print("Watermark embedded successfully")
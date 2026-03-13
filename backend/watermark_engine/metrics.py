# import cv2
# import numpy as np
# from skimage.metrics import structural_similarity as ssim


# def calculate_metrics(original_path, suspicious_path):
#     img1 = cv2.imread(original_path)
#     img2 = cv2.imread(suspicious_path)
    
#     if img1 is None:
#             raise Exception(f"Could not load original image: {original_path}")

#     if img2 is None:
#         raise Exception(f"Could not load suspicious image: {suspicious_path}")
#     img1 = cv2.resize(img1, (512, 512))
#     img2 = cv2.resize(img2, (512, 512))

#     mse_value = np.mean((img1 - img2) ** 2)

#     if mse_value == 0:
#         psnr_value = 100
#     else:
#         psnr_value = 20 * np.log10(255.0 / np.sqrt(mse_value))

#     ssim_value = ssim(
#         cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY),
#         cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#     )

#     return {
#         "mse": float(mse_value),
#         "psnr": float(psnr_value),
#         "ssim": float(ssim_value)
#     }



import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_metrics(original_path, suspicious_path):

    img1 = cv2.imread(original_path)
    img2 = cv2.imread(suspicious_path)

    if img1 is None:
        raise Exception(f"Could not load original image: {original_path}")

    if img2 is None:
        raise Exception(f"Could not load suspicious image: {suspicious_path}")

    img1 = cv2.resize(img1, (512, 512))
    img2 = cv2.resize(img2, (512, 512))

    mse_value = np.mean((img1 - img2) ** 2)

    if mse_value == 0:
        psnr_value = 100
    else:
        psnr_value = 20 * np.log10(255.0 / np.sqrt(mse_value))

    ssim_value = ssim(
        cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY),
        cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    )

    return {
        "mse": float(mse_value),
        "psnr": float(psnr_value),
        "ssim": float(ssim_value)
    }
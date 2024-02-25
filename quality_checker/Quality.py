import numpy as np
from skimage.metrics import structural_similarity
import math
import cv2
import npyscreen

class Quality:
    def mse(img1, img2):
        try:
            err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
            err /= float(img1.shape[0] * img2.shape[1])
            return err
        except Exception as e:
            try:
                npyscreen.notify_confirm(f"Błąd w funkcji mse: {e}")
            except:
                print(f"Błąd w funkcji mse: {e}")
            return None

    def psnr(img1, img2):
        try:
            mse = Quality.mse(img1, img2)
            if mse == 0:
                return 100
            else:
                PIXEL_MAX = 255.0
                return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
        except Exception as e:
            try:
                npyscreen.notify_confirm(f"Błąd w funkcji psnr: {e}")
            except:
                print(f"Błąd w funkcji psnr: {e}")
            return None

    def minkowski(img1, img2, p):
        try:
            return np.sum(np.abs(img1 - img2) ** p) ** (1 / p)
        except Exception as e:
            try:
                npyscreen.notify_confirm(f"Błąd w funkcji minkowski: {e}")
            except:
                print(f"Błąd w funkcji minkowski: {e}")
            return None

    def snr(img1, img2):
        try:
            signal = np.mean((img1*255) ** 2)
            noise = Quality.mse(img1, img2)
            return 10 * np.log10(signal / noise)
        except Exception as e:
            try:
                npyscreen.notify_confirm(f"Błąd w funkcji snr: {e}")
            except:
                print(f"Błąd w funkcji snr: {e}")
            return None

    def ssim(img1, img2, win_size=3):
        try:
            ssim = structural_similarity(img1, img2, full=True, win_size=win_size)
            return ssim[0]
        except Exception as e:
            try:
                npyscreen.notify_confirm(f"Błąd w funkcji ssim: {e}")
            except:
                print(f"Błąd w funkcji ssim: {e}")
            return None

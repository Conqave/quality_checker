import cv2
import numpy as np
import npyscreen
import json
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity
from Quality import *
from Image import *

class ImageApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name="Image Quality Comparison")

class MainForm(npyscreen.ActionFormMinimal):
    def save_history(self, image1_path, image2_path):
        try:
            with open('history.json', 'r') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        history.append((image1_path, image2_path))

        with open('history.json', 'w') as f:
            json.dump(history, f)

    def load_history(self):
        try:
            with open('history.json', 'r') as f:
                history = json.load(f)
                if history == '':
                    history = []
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        return [f"{image1}, {image2}" for image1, image2 in history]

    def create(self):
        self.image1_path = self.add(npyscreen.TitleFilenameCombo, name="Image 1:")
        self.image2_path = self.add(npyscreen.TitleFilenameCombo, name="Image 2:")
        self.history = self.add(npyscreen.TitleSelectOne, max_height=4, name="History:", values=self.load_history(), scroll_exit=True)

    def on_ok(self):
        
        try:
            if self.history.value and not (self.image1_path.value or self.image2_path.value):
                self.image1_path.value, self.image2_path.value = self.history.values[self.history.value[0]].split(', ')
                image1, image2 = Image.readImage(self.image1_path.value, self.image2_path.value)
                self.save_history(self.image1_path.value, self.image2_path.value)
            else:
                image1, image2 = Image.readImage(self.image1_path.value, self.image2_path.value)
                #npyscreen.notify_confirm(f"Sources: {str(self.image1_path.value)}", title="Error")
                #npyscreen.notify_confirm(f"Sources: {str(self.image2_path.value)}", title="Error")

                self.save_history(self.image1_path.value, self.image2_path.value)

        except Exception as e:
            npyscreen.notify_confirm(f"Error reading images: {str(e)}", title="Error")
            return

        try:
            mse = Quality.mse(image1, image2)
            psnr = Quality.psnr(image1, image2)
            ssim = Quality.ssim(image1, image2)
            snr = Quality.snr(image1, image2)
            minkowskiEuklides = Quality.minkowski(image1, image2, 2)
            minkowskiManhattan = Quality.minkowski(image1, image2, 1)
        except Exception as e:
            npyscreen.notify_confirm(f"Error calculating quality metrics: {str(e)}", title="Error")
            return

        #npyscreen.notify_confirm(f"MSE: {mse}\nPSNR: {psnr}\nSSIM: {ssim}\nSNR: {snr}\nMinkowski Euklides: {minkowskiEuklides}\nMinkowski Manhattan: {minkowskiManhattan}", title="Image Quality Comparison Results")
        npyscreen.notify_confirm(f"MSE: {mse}\nPSNR: {psnr}\nSSIM: {ssim}\n", title="Image Quality Comparison Results")

if __name__ == "__main__":
    try:
        app = ImageApplication()
        app.run()
    except Exception as e:
        print(f"Error running application: {str(e)}")

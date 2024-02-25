import os
import cv2
from prettytable import PrettyTable

import sys
sys.path.insert(1, './quality_checker')
from Quality import *

path = "./resoult_images/"

def read_png_files(folder):
    return [plik for plik in os.listdir(folder) if plik.lower().endswith('.png')]

def find_original(files):
    for i in files:
        if i.lower().startswith('oryginal'):
            return i    
    return None

def main():
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for folder in folders:
        pliki = read_png_files(os.path.join(path, folder))
        original = find_original(pliki)
        table = PrettyTable()
        table.field_names = ["Nazwa", "MSE", "PSNR", "SSIM"]
        img0 = cv2.imread(os.path.join(path, folder, original))

        for i in pliki:
            img1 = cv2.imread(os.path.join(path, folder, i))
            if(img0.shape[0]==img1.shape[0] and img0.shape[1]==img1.shape[1]):
                round_number = 4
                table.add_row([i, round(Quality.mse(img0, img1), round_number), round(Quality.psnr(img0, img1), round_number), round(Quality.ssim(img0, img1), round_number)])
        print(f"Table for folder {folder}:")
        print(table)
        print("\n")


if __name__ == "__main__":
    main()

import npyscreen
import cv2

class FileSelector(npyscreen.Form):
    def create(self):
        self.file = self.add(npyscreen.TitleFilenameCombo, name="Wybierz plik:")

class Image:
    bvalues = ["Obraz pierwszy","Obraz drugi"]
    def readImage(img_path1, img_path2):
        img1 = img2 = None
        try:
            img1 = cv2.imread(img_path1)
            img2 = cv2.imread(img_path2)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        except Exception as e:
            npyscreen.notify_confirm(f"Wystąpił problem z wczytaniem obrazów: {e}", title="Błąd", wrap=True, editw=1)
            return None, None

        if img1 is not None and img2 is not None and img1.shape != img2.shape:
            npyscreen.notify_confirm("Obrazy nie mają takich samych wymiarów, wybierz je ponownie.", title="Błąd", wrap=True, editw=1)
            return None, None
        else:
            return img1, img2
            
    def selectImageToShow():
        F  = npyscreen.Form(name = "Zobacz wczytane obrazy",)
        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Wybierz",
                values = Image.bvalues, scroll_exit=True)
        F.edit()
        return ms2.get_selected_objects()

    def getBValues():
        return Image.bvalues
    
    def showImage(img):
        try:
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            npyscreen.notify_wait(f"Wystąpił błąd: {e}", title="Błąd", wrap=True, editw=1)

import sys
import os
import cv2
import numpy as np

# SDK Importlari
try:
    from sdks.novavision.src.media.image import Image
    from sdks.novavision.src.base.capsule import Capsule
    from sdks.novavision.src.helper.executor import Executor
except ImportError:
    # Lokal test icin bos siniflar
    class Capsule:
        def __init__(self, r, b): self.request, self.redis_db = r, b


    class Executor:
        pass


    class Image:
        pass

# Modeli projeden cekiyoruz
try:
    from capsules.DemoPackage.src.models.PackageModel import PackageModel
except ImportError:
    # Lokal calisma icin alternatif yol
    from src.models.PackageModel import PackageModel


class Filter(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # Giriş resmini al
        self.image_input = self.request.get_param("inputImageOne")

        # Mod seç
        self.filter_mode_wrapper = self.request.get_param("configFilterMode")
        self.mode_name = self.filter_mode_wrapper.value

        # Blur seçildiyse
        if self.mode_name == "Blur":
            self.kernel_size = self.request.get_param("blurKernelSize")
            self.is_gaussian = self.request.get_param("blurIsGaussian")

        # Threshold seçildiyse
        elif self.mode_name == "Threshold":
            self.thresh_value = self.request.get_param("threshValue")
            self.thresh_type = self.request.get_param("threshType")

    def process_image(self, img_array):
        if img_array is None: return None

        # Blur Islemi
        if self.mode_name == "Blur":
            try:
                k_size = int(self.kernel_size)
            except:
                k_size = 5

            if k_size % 2 == 0: k_size += 1

            if self.is_gaussian:
                processed = cv2.GaussianBlur(img_array, (k_size, k_size), 0)
            else:
                processed = cv2.blur(img_array, (k_size, k_size))
            return processed

        # Threshold Islemi
        elif self.mode_name == "Threshold":
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            try:
                t_val = float(self.thresh_value)
            except:
                t_val = 127.0

            _, processed = cv2.threshold(gray, t_val, 255, cv2.THRESH_BINARY)
            processed_color = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
            return processed_color

        return img_array

    def run(self):
        img_obj = Image.get_frame(img=self.image_input, redis_db=self.redis_db)
        img_array = img_obj.value

        result_array = self.process_image(img_array)
        img_obj.value = result_array

        response = {
            "outputs": {
                "outputImageOne": img_obj
            }
        }
        return response


if "__main__" == __name__:
    Executor(sys.argv[1]).run()

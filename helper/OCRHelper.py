import os
import pytesseract
from PIL import ImageGrab, ImageDraw
import time


class OCRHelper:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.ensure_dir(self.data_folder)
        self.config = "--oem 1 --psm 11"

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_ocr_result(self, image):
        """Perform OCR and return the results."""
        return pytesseract.image_to_data(
            image, lang="eng", config=self.config, output_type=pytesseract.Output.DICT
        )

    def filter_ocr_result(self, word, ocr_result):
        """Filter OCR results to include only entries matching a specific word."""
        # Initialize a dictionary to hold filtered OCR results, with the same structure as ocr_result
        filtered_ocr_result = {key: [] for key in ocr_result.keys()}

        # Get the total number of entries in the OCR results
        total_entries = len(ocr_result["text"])

        # Iterate through all entries
        for i in range(total_entries):
            # Check if the current text matches the specified word (case-insensitive)
            if word.lower() == ocr_result["text"][i].lower():
                # If a match is found, append the data for this entry to the corresponding lists in the filtered dictionary
                for key in ocr_result.keys():
                    filtered_ocr_result[key].append(ocr_result[key][i])

        return filtered_ocr_result

    def draw_ocr_result(self, image, ocr_result):
        """Draw bounding boxes on the image based on OCR results."""
        image_copy = image.convert("RGB")
        draw = ImageDraw.Draw(image_copy)
        for i, conf in enumerate(ocr_result["conf"]):
            if int(conf) > 50:  # Confidence threshold
                (x, y, w, h) = (
                    ocr_result["left"][i],
                    ocr_result["top"][i],
                    ocr_result["width"][i],
                    ocr_result["height"][i],
                )
                draw.rectangle(((x, y), (x + w, y + h)), outline="red")
        return image_copy

    def wait_for_word(self, word, timeout=None):
        """Wait for a word to appear on the screen, then highlight it."""
        start_time = time.time()
        while True:
            if timeout and time.time() - start_time > timeout:
                print("Timeout reached, word not found.")
                break
            screen = ImageGrab.grab()
            ocr_result = self.get_ocr_result(screen)
            match_result = self.filter_ocr_result(word, ocr_result)
            if len(match_result["conf"]) > 0:
                highlighted_image = self.draw_ocr_result(screen, match_result)
                highlighted_image.save(
                    os.path.join(self.data_folder, f"{word}_highlighted.png")
                )
                print(f"Word '{word}' found and highlighted.")
                break
            time.sleep(1)  # Avoid too high frequency


if __name__ == "__main__":
    agent = OCRHelper()
    agent.wait_for_word("python", timeout=10)

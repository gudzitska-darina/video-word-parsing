import os
import cv2
import pytesseract as pytesseract


def break_name(dir):
    file_list = sorted(os.listdir(dir))
    for i, file in enumerate(file_list):
        if file.endswith('.mp4'):
            os.rename(os.path.join(dir, file), os.path.join(dir, "VIDEO_"+str(i)+".mp4"))


def renaming_video(path, file, word, sp, t):
    #alarm clock_atlas_d.mp4
    pattern = f"{word}_{sp}_{t}.mp4"
    os.rename(os.path.join(path, file), os.path.join(path, pattern))


def processing_img(img_p):
    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(img_p)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    return invert


def create_frame(path, video_name):
    cap = cv2.VideoCapture(os.path.join(path, video_name)) # video_name is the video being called
    cap.set(1, 300)  # Where frame_no is the frame you want
    ret, frame = cap.read()  # Read the frame
    cropped = frame[950:1070, 300:1700]
    image_path = os.path.join(path, 'frame.png')
    cv2.imwrite(image_path, cropped)

    final_img = processing_img(image_path)
    os.remove(image_path)
    return final_img


def creating_str(img):
    data = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
    return data[:-1]


def main():
    NAME_DIR = '/Users/darinagudzitska/Desktop/CONVERTED'
    SPEAKER = "joe"
    if not os.path.isdir(NAME_DIR):
        FileNotFoundError

    # break_name(NAME_DIR)

    file_list = sorted(os.listdir(NAME_DIR))
    prev_word = "None"
    for file in file_list:
        if file.endswith(".mp4"):
            frame = create_frame(NAME_DIR, file)
            word = creating_str(frame)

            type_w = 'q' if word == '22?' else 'd'
            if type_w == 'q':
                word = prev_word

            renaming_video(NAME_DIR, file, word.lower(), SPEAKER, type_w)
            prev_word = word


if __name__ == '__main__':
    main()



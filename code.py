import cv2
from ultralytics import YOLO
from PIL import Image, ImageEnhance

def show(frame, chk):
    if chk:
        cv2.imshow('wow', frame)
        cv2.waitKey(0)

def preprocessing(frame, chk):
    show(frame, chk)
    cv2.imwrite('frame.jpg', frame)
    im = Image.open('frame.jpg')
    enh = ImageEnhance.Contrast(im)
    output = enh.enhance(1.5) #повышаем контрастность фрагмента в 3 раза 
    output.save('frame.jpg')
    frame = cv2.imread('frame.jpg')
    show(frame, chk)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #накладываем черно-белый фильтр
    show(frame, chk)
    cv2.destroyAllWindows()
    cv2.imwrite('frame.jpg', frame)

def count_people(image_path):
    model = YOLO('yolov8n.pt') 
    preprocessing(cv2.imread(image_path), 1)
    image = cv2.imread('frame.jpg')
    results = model(image)
    person_count = 0
    for result in results:
        boxes = result.boxes.xyxy  # Получение координат боксов
        classes = result.boxes.cls  # Получение классов объектов
        for box, cls in zip(boxes, classes):
            # Проверяем, что обнаруженный объект - человек
            if int(cls) == 0: 
                person_count += 1
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Отображение результата
    show(image, chk)
    cv2.destroyAllWindows()
    print(f"Количество людей на изображении: {person_count}")


# Face Recognition System with Raspberry Pi Camera

This project demonstrates a face recognition system using a Raspberry Pi camera. Below are the key parts of the code, focusing on the **imports** and the **fundamentals** of facial detection and recognition.

---

## 1. Image Capture

### Imports
```python
import cv2
import os
from datetime import datetime
from picamera2 import Picamera2
import time
```

### Key Function: `capture_photos`
This function captures images using the Raspberry Pi camera and saves them to a folder.

```python
def capture_photos(name):
    folder = create_folder(name)
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()
    time.sleep(2)  # Camera warm-up

    while True:
        frame = picam2.capture_array()
        cv2.imshow('Capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # Save photo on spacebar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            cv2.imwrite(os.path.join(folder, filename), frame)
        
        elif key == ord('q'):  # Quit on 'q'
            break
    
    picam2.stop()
    cv2.destroyAllWindows()
```

---

## 2. Face Encoding

### Imports
```python
import os
from imutils import paths
import face_recognition
import pickle
import cv2
```

### Key Function: Generate Encodings
This processes images to detect faces and generate encodings.

```python
imagePaths = list(paths.list_images("dataset"))
knownEncodings = []
knownNames = []

for imagePath in imagePaths:
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

# Save encodings to a file
with open("encodings.pickle", "wb") as f:
    pickle.dump({"encodings": knownEncodings, "names": knownNames}, f)
```

---

## 3. Real-Time Face Detection

### Imports
```python
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import face_recognition
```

### Key Function: `detect_faces`
This function detects and recognizes faces in real-time.

```python
def detect_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.07, minNeighbors=6, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face_encoding = face_recognition.face_encodings(rgb_frame, [(y, x+w, y+h, x)])
        if face_encoding:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding[0])
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_name[first_match_index]
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return frame
```

### Real-Time Loop
This captures frames from the camera and processes them for face detection.

```python
while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = detect_faces(frame)
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.close()
cv2.destroyAllWindows()
```

---

## Key Takeaways

1. **Image Capture**:
   - Uses `Picamera2` to capture images.
   - Saves images with timestamps for training.

2. **Face Encoding**:
   - Detects faces using HOG (Histogram of Oriented Gradients).
   - Generates and saves face encodings using `face_recognition`.

3. **Real-Time Detection**:
   - Uses Haar Cascade for initial face detection.
   - Compares detected faces with pre-trained encodings for recognition.
   - Displays bounding boxes and names in real-time.

This system is modular and can be extended for various applications like attendance systems or security systems.
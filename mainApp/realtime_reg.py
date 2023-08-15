from ultralytics import YOLO
import cv2
import numpy as np

model=YOLO('./best.pt')
list=set()
vid=cv2.VideoCapture(0)

while True:
    ret,frame=vid.read()
    if ret:
        results=model(frame)
        names=model.names
        annoted_frame=results[0].plot()
        
        for r in results:
            for b in r.boxes:
                if b.conf>=0.5:
                    list.add(names[int(b.cls)])
                
        cv2.imshow("YOLOv8 Interface",annoted_frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
vid.release()
cv2.destroyAllWindows()

print(list)
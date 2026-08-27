from ultralytics import  YOLO

class YOLOPredictor:
    def __init__(self,weight_path,device="cpu"):
        self.model = YOLO(weight_path)

        self.device = device

        self.class_names = self.model.names

    def predict(self,frame):
        results = self.model(frame,verbose=False)
        return results[0]
        detections = []
        for cox in result.boxes:
            cls = int(box.cld.item())
            conf = float(box.conf.item())
            x1,y1,x2,y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id:":cls,
                "class_name": self.class_names[cls],
                "confidence": conf,   
                "bbox":[
                    int(x1),
                    int(y2),
                    int(x2),
                    int(y2)
                ]
         })
        return detections

    def predict_frame(self,frame):
        return self.predict(frame)
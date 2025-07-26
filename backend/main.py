from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import ARRAY, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import cv2
import base64
from deepface import DeepFace
import os 
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
Base = declarative_base()

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FaceData(BaseModel):
    vectors: list[list[float]] 
    fileNames: list[str]  

class FileModel(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filedata = Column(LargeBinary)
    individuals = Column(ARRAY(String), nullable=True)

class FaceEmbedder:
    def __init__(self):
        dummy_img = np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
        try:
            DeepFace.represent(dummy_img, model_name="Facenet", enforce_detection=False)
        except:
            pass
    
    def extract_face_embedding(self, image):
        try:

            embedding = DeepFace.represent(
                image, 
                model_name="Facenet", 
                enforce_detection=False,
                detector_backend='skip',
                align=False
            )


            return embedding[0]["embedding"]
        except Exception:
            return None

_embedder = FaceEmbedder()

def extract_face_embedding(image):
    return _embedder.extract_face_embedding(image)

def preprocessor(file_content: bytes, face_context: dict) -> list:
        start_time = time.time()
        image_array = np.frombuffer(file_content, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            return []
            

        cropped_faces = detect_crop_faces(image)

        person_labels = []

        for face in cropped_faces:
            embedding = extract_face_embedding(face)

            if embedding is None:
                continue
            
            if face_context["embeddings"]:
                similarities = cosine_similarity([embedding], face_context["embeddings"])
                max_similarity_index = similarities.argmax()
                max_similarity = similarities[0][max_similarity_index]

                if max_similarity > 0.6:
                    person_labels.append(face_context["labels"][max_similarity_index])
                    continue
            new_label = f"Person {len(face_context['labels']) + 1}"
            face_context["embeddings"].append(embedding)
            face_context["labels"].append(new_label)
            face_context["face"].append(face)
            person_labels.append(new_label)
        end_time = time.time()
        print("run time =" + str(end_time-start_time))
        return person_labels


def detect_crop_faces(image):
    try:
        face_objs = DeepFace.extract_faces(image, detector_backend="opencv")

    except Exception:
        return []
    cropped_faces = []
    for face_obj in face_objs:
        x, y, w, h = face_obj["facial_area"]["x"], face_obj["facial_area"]["y"], \
                      face_obj["facial_area"]["w"], face_obj["facial_area"]["h"]
        cropped_face = image[y:y+h, x:x+w]
        cropped_faces.append(cropped_face)
    return cropped_faces

def detect_crop_faces_optimized(image):
    """
    Optimized version with multiple improvements but less accurate
    """
    start_time = time.time()
    
    try:
        face_objs = DeepFace.extract_faces(
            image, 
            detector_backend="opencv",
            enforce_detection=False,
            align=False
        )
    except Exception as e:
        print(f"Face detection failed: {e}")
        return []
    
    if not face_objs:
        return []
    
    cropped_faces = []
    
    for face_obj in face_objs:
        facial_area = face_obj["facial_area"]
        x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
        
        img_height, img_width = image.shape[:2]
        x = max(0, min(x, img_width))
        y = max(0, min(y, img_height))
        w = min(w, img_width - x)
        h = min(h, img_height - y)
        
        if w > 0 and h > 0:
            cropped_face = image[y:y+h, x:x+w]
            cropped_faces.append(cropped_face)
    
    end_time = time.time()
    print(f"Face detection runtime: {end_time - start_time:.3f}s, found {len(cropped_faces)} faces")
    return cropped_faces

@app.post("/extract")
async def extract_faces(files: list[UploadFile] = File(...)):
    try:
        if not files:
            return JSONResponse(content={"message": "No files uploaded"}, status_code=400)
        
        face_context = {
            "embeddings": [],
            "labels": [],
            "face": [],
        }
        
        uploaded_files = []
        
        for file in files:
            file_content = await file.read()
            person_attributes = preprocessor(file_content, face_context)
            
            result = {
                "filename": file.filename,
                "individuals": person_attributes
            }
            uploaded_files.append(result)
            
            del file_content
        
        unique_faces = {}
        seen_labels = set()
        
        for label, face_img in zip(face_context["labels"], face_context["face"]):
            if label not in seen_labels:
                seen_labels.add(label)
                unique_faces[label] = base64.b64encode(cv2.imencode('.jpg', face_img)[1]).decode('utf-8')
        
        response_data = {
            "result": uploaded_files,
            "people_faces": [
                {"label": label, "face": img_b64} 
                for label, img_b64 in unique_faces.items()
            ]
        }

        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

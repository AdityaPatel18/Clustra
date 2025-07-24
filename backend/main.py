from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.cluster import DBSCAN
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from pydantic import BaseModel
from typing import Dict
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import ARRAY, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import cv2
import base64
import numpy as np
from fastapi import FastAPI
from contextlib import asynccontextmanager
import numpy as np
from deepface import DeepFace
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.post("/clusterr")
def cluster_faces(data: FaceData):


    vectors = np.array(data.vectors)
    file_names = data.fileNames

    if len(vectors) != len(file_names):
        return {"error": "Mismatch between number of vectors and filenames."}

    # Initialize clustering context
    clustered_embeddings = []
    clustered_labels = []
    image_to_people: Dict[str, set] = {}

    for vector, filename in zip(vectors, file_names):
        if clustered_embeddings:
            sims = cosine_similarity([vector], clustered_embeddings)[0]
            max_sim_index = np.argmax(sims)
            max_sim = sims[max_sim_index]

            if max_sim > 0.6:
                person = clustered_labels[max_sim_index]
            else:
                person = f"Person {len(set(clustered_labels)) + 1}"
                clustered_embeddings.append(vector)
                clustered_labels.append(person)
        else:
            person = "Person 1"
            clustered_embeddings.append(vector)
            clustered_labels.append(person)

        if filename not in image_to_people:
            image_to_people[filename] = set()
        image_to_people[filename].add(person)

    # Convert sets to lists
    result = {
        "clustered": {filename: list(people) for filename, people in image_to_people.items()},
        "people": list(set(clustered_labels))
    }

    return result


def extract_face_embedding(image):
    try:
        embedding = DeepFace.represent(image, model_name="Facenet", enforce_detection=False)
        return embedding[0]["embedding"]
    except Exception:
        return None

def preprocessor(file_content: bytes, face_context: dict) -> list:
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

@app.post("/extract")
async def extract_faces(files: list[UploadFile] = File(...)):
    try:
        if not files:
            return JSONResponse(content={"message": "No files uploaded"}, status_code=400)
        
        uploaded_files = []
        face_context = {
            "embeddings": [],
            "labels": [],
            "face": [],
        }
        for file in files:
            file_content = await file.read()

            person_attributes = preprocessor(file_content, face_context)
            result = FileModel(
                filename=file.filename, 
                filedata=file_content,
                individuals = person_attributes
            )
            uploaded_files.append(result)
        
        # Build response data
        response_data = {
            "result": [
                {
                    "filename": f.filename,
                    "individuals": f.individuals
                } for f in uploaded_files
            ]
        }

        unique_faces = {
            label: base64.b64encode(cv2.imencode('.jpg', face_img)[1]).decode('utf-8')
            for label, face_img in zip(face_context["labels"], face_context["face"])
            if label not in face_context["labels"][:face_context["labels"].index(label)]
        }
        response_data["people_faces"] = [
            {"label": label, "face": img_b64} for label, img_b64 in unique_faces.items()
        ]

        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")
 
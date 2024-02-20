from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils import load_classifiers,read_imagefile,predict
app = FastAPI()
model,face_cascade,leye_cascade,reye_cascade=load_classifiers()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict')
async def drowsiness_api(image: UploadFile=File(...)):
    print("Image received")
    image = read_imagefile(await image.read())
    status,leye,reye=predict(image,model,face_cascade,leye_cascade,reye_cascade)
    if not status:
        return {"status":0}

    if leye=="Closed" and reye=="Closed":
        return {"status":1, "prediction":"Drowsiness Detected","pred":1}
    elif (leye=="Open" and reye=="Closed") or (leye=="Closed" and reye=="Open"):
        return {"status":1, "prediction":"Maybe Drowsy","pred":1}
    else:
        return {"status":1, "prediction":"No Drowsiness Detected","pred":0}

if __name__ == "__main__":
    uvicorn.run(app)

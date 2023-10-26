uvicorn main:app --reload
docker build -t ocr-text-detection-backend .
docker run -p 4202:80 -it ocr-text-detection-backend

import pytube  # pip install pytube
from fastapi import FastAPI, Request  # pip install fastapi
from fastapi.responses import HTMLResponse,FileResponse  # pip install
from fastapi.templating import Jinja2Templates  # pip install fastapi
import uvicorn  # pip install uvicorn
import os
import tempfile
import multipart # pip install python-multipart    
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/download", response_class=HTMLResponse)
def download(request: Request):
    # url 입력창과 download 버튼이 있는 메인페이지를 반환합니다.
    return templates.TemplateResponse("download.html", {"request": request})





@app.post("/download")
async def download_youtube_video(request: Request):
    print("download_youtube_video")
    # 유튜브 url을 받아서 영상을 다운로드하고 mp4 파일을 반환합니다.
    form = await request.form()
    url = form.get('url')
    youtube = pytube.YouTube(url)
    video = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    # 임시 디렉토리에 비디오를 다운로드합니다.
    tmpdirname = tempfile.mkdtemp()
    print(tmpdirname)
    if not os.path.exists(tmpdirname):
        os.makedirs(tmpdirname)
    
    video_path = video.download(tmpdirname)
    response = FileResponse(video_path, media_type='video/mp4', filename=os.path.basename(video_path))
    
    # 임시 파일을 삭제합니다.
    # try:
    #     os.remove(video_path)
    # except FileNotFoundError:
    #     pass
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

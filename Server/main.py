import uvicorn
from fastapi import FastAPI, File, UploadFile
from utils import *
from starlette.responses import FileResponse

app = FastAPI()


@app.post("/archive_upload/")
async def archive_upload(file: UploadFile = File(...)):
    try:
        archive = await file.read()
        print(file.filename)
        if check_filename(file.filename):
            with open('./Archive/{}'.format(file.filename), 'wb') as f:
                f.write(archive)
            return 'success'
        else:
            return 'file name is not appropriate!'
    except Exception as e:
        return "Error:{}".format(e)


@app.get("/get_archives_info/")
async def get_archives_info():
    try:
        return {'info': archives_info()}
    except Exception as e:
        return 'Error:{}'.format(e)


@app.get("/archive_download/{filename}/")
async def download_archive(filename):
    try:
        if os.path.exists('./Archive/{}'.format(filename)):
            return FileResponse('./Archive/{}'.format(filename))
        else:
            return 'No Archive named {}!'.format(filename)
    except Exception as e:
        return "Error:{}".format(e)


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port='41356', workers=1)

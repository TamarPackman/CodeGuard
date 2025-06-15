from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import services.alerts_handler as alerts_handler
import services.common_analysis as common_analysis
import json
router = APIRouter()
@router.post("/alerts")
async def alerts(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Please upload a zip file"})
    try :
     python_files = await common_analysis.extract_python_files(file)
    except OSError as e:
     return JSONResponse(status_code=400, content={"error": e})
    results = {}
    for py_file,source_code in python_files.items():
        alerts_handler.get_alerts_data(py_file,source_code,results)
        json.dumps(results)
    return JSONResponse(status_code=200, content=results)



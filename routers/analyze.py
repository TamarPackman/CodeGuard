from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
import matplotlib.pyplot as plt
import io
import services.analyzer as analyzer
import services.common_analysis as common_analysis

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Please upload a zip file"})
    try:
      python_files= await common_analysis.extract_python_files(file)
    except OSError as e:
      return JSONResponse(status_code=400, content={"error": e})

    analyze_data=u=analyzer.get_analysis_data(python_files)
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    axs[0].bar(analyze_data["function_lengths"].keys(), analyze_data["function_lengths"].values(), color='skyblue')
    axs[0].set_title('Distribution of function lengths')
    axs[0].set_xlabel('function name')
    axs[0].set_ylabel('function length')
    axs[0].tick_params(axis='x', rotation=45)

    axs[1].pie(analyze_data["issue_counts_by_type"].values(), labels=analyze_data["issue_counts_by_type"].keys(), autopct='%1.1f%%', startangle=90)
    axs[1].set_title('Number of issues per issue type')

    # תרשים עמודות
    axs[2].bar(analyze_data["detailed_file_issues"].keys(), analyze_data["detailed_file_issues"].values(), color='lightgreen')
    axs[2].set_title('Number of issues per file')
    axs[2].set_xlabel('file')
    axs[2].set_ylabel('Number of issues')
    axs[2].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    return StreamingResponse(img, media_type="image/png")

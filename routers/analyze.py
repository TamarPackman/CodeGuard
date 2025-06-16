from fastapi import APIRouter, UploadFile, File,Form
from fastapi.responses import StreamingResponse, JSONResponse
import matplotlib.pyplot as plt
import io
import services.analyzer as analyzer
import services.common_analysis as common_analysis
import json
from datetime import datetime
import os
from matplotlib.ticker import MaxNLocator

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...),target_path: str = Form(...)):
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"error": "Please upload a zip file"})
    try:
      python_files= await common_analysis.extract_python_files(file)
    except OSError as e:
      return JSONResponse(status_code=400, content={"error": e})
    analyze_data=analyzer.get_analysis_data(python_files)
    issue_file_path = os.path.join(target_path, "Issue tracking.json")

    if os.path.isfile(issue_file_path):
        with open(issue_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    issues_to_add=sum(analyze_data["detailed_file_issues"].values())
    print(issues_to_add)
    if current_time in data:
        data[current_time] += issues_to_add
    else:
        data[current_time] = issues_to_add
    with open(issue_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(issue_file_path, "r", encoding="utf-8") as f:
        issues_by_time = json.load(f)
    sorted_items = sorted(issues_by_time.items())
    dates = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    fig, axs = plt.subplots(1, 4, figsize=(24, 6))  # שימי לב ל־4 גרפים

    # גרף 1 – אורכי פונקציות
    axs[0].bar(analyze_data["function_lengths"].keys(), analyze_data["function_lengths"].values(), color='skyblue')
    axs[0].set_title('Distribution of function lengths')
    axs[0].set_xlabel('Function name')
    axs[0].set_ylabel('Function length')
    axs[0].tick_params(axis='x', rotation=45)

    # גרף 2 – סוגי בעיות
    axs[1].pie(analyze_data["issue_counts_by_type"].values(),
               labels=analyze_data["issue_counts_by_type"].keys(),
               autopct='%1.1f%%', startangle=90)
    axs[1].set_title('Number of issues per issue type')

    # גרף 3 – מספר בעיות לפי קובץ
    axs[2].bar(analyze_data["detailed_file_issues"].keys(), analyze_data["detailed_file_issues"].values(),
               color='lightgreen')
    axs[2].set_title('Number of issues per file')
    axs[2].set_xlabel('File')
    axs[2].set_ylabel('Number of issues')
    axs[2].tick_params(axis='x', rotation=45)

    # גרף 4 – גרף קווי של בעיות לפי זמן
    axs[3].plot(dates, counts, marker='o', color='orange')
    axs[3].set_title("Issues over time")
    axs[3].set_xlabel("Time")
    axs[3].set_ylabel("Issues")
    axs[3].tick_params(axis='x', rotation=45)
    axs[3].yaxis.set_major_locator(MaxNLocator(integer=True))
    # שמירה והחזרה
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)

    return StreamingResponse(img, media_type="image/png")

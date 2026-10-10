import fitz  # PyMuPDF
import spacy
import re
import pytesseract
from pdf2image import convert_from_bytes
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
from pydantic import BaseModel
from typing import List
import json
import io
import uvicorn

app = FastAPI(title="AI Document Redaction & Metadata Extraction Engine")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy NLP Model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Regex patterns for sensitive identifiers
REGEX_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "AADHAAR": r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"
}

def process_scanned_page(page, page_num):
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    ocr_data = pytesseract.image_to_data(
        convert_from_bytes(img_bytes)[0], 
        output_type=pytesseract.Output.DICT
    )
    
    extracted_text = " ".join([word for word in ocr_data['text'] if word.strip()])
    boxes = []
    n_boxes = len(ocr_data['text'])
    
    for i in range(n_boxes):
        if int(ocr_data['conf'][i]) > 30 and ocr_data['text'][i].strip():
            boxes.append({
                "word": ocr_data['text'][i],
                "x0": ocr_data['left'][i],
                "y0": ocr_data['top'][i],
                "x1": ocr_data['left'][i] + ocr_data['width'][i],
                "y1": ocr_data['top'][i] + ocr_data['height'][i],
                "page": page_num
            })
    return extracted_text, boxes


@app.post("/api/analyze")
async def analyze_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PDF or unsupported document format.")
    
    full_text = ""
    suggested_redactions = []
    
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text()
        
        if not text.strip():
            text, _ = process_scanned_page(page, page_idx)
            
        full_text += f"\n--- Page {page_idx + 1} ---\n" + text

        for entity_type, pattern in REGEX_PATTERNS.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                matching_text = match.group()
                rects = page.search_for(matching_text)
                for rect in rects:
                    suggested_redactions.append({
                        "id": f"reg-{page_idx}-{rect.x0}-{rect.y0}",
                        "page": page_idx,
                        "type": entity_type,
                        "text": matching_text,
                        "confidence": 0.98,
                        "bbox": {"x0": rect.x0, "y0": rect.y0, "x1": rect.x1, "y1": rect.y1}
                    })

        doc_nlp = nlp(text)
        for ent in doc_nlp.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "MONEY"]:
                rects = page.search_for(ent.text)
                for rect in rects:
                    suggested_redactions.append({
                        "id": f"ner-{page_idx}-{rect.x0}-{rect.y0}",
                        "page": page_idx,
                        "type": ent.label_,
                        "text": ent.text,
                        "confidence": 0.88,
                        "bbox": {"x0": rect.x0, "y0": rect.y0, "x1": rect.x1, "y1": rect.y1}
                    })

    nlp_summary = nlp(full_text[:5000])
    metadata = {
        "page_count": len(doc),
        "parties_involved": list(set([ent.text for ent in nlp_summary.ents if ent.label_ in ["PERSON", "ORG"]])),
        "dates_mentioned": list(set([ent.text for ent in nlp_summary.ents if ent.label_ == "DATE"])),
        "monetary_values": list(set([ent.text for ent in nlp_summary.ents if ent.label_ == "MONEY"])),
    }

    return {
        "status": "success",
        "metadata": metadata,
        "suggested_redactions": suggested_redactions,
        "total_redactions_found": len(suggested_redactions)
    }


@app.post("/api/redact-and-export")
async def redact_and_export(
    file: UploadFile = File(...), 
    redactions_json: str = Form(...)
):
    file_bytes = await file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    redactions_list = json.loads(redactions_json)
    
    for item in redactions_list:
        page_num = item["page"]
        bbox = item["bbox"]
        
        if page_num < len(doc):
            page = doc[page_num]
            rect = fitz.Rect(bbox["x0"], bbox["y0"], bbox["x1"], bbox["y1"])
            
            page.add_redact_annot(rect, fill=(0, 0, 0))
            page.apply_redactions()

    doc.set_metadata({})
    for page in doc:
        page.clean_contents()

    output_stream = io.BytesIO()
    doc.save(output_stream, garbage=4, deflate=True, clean=True)
    doc.close()
    
    output_stream.seek(0)
    
    return Response(
        content=output_stream.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sanitized_redacted.pdf"}
    )


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Document Redaction & Metadata Studio</title>
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 font-sans">
        <div id="root"></div>

        <script type="text/babel">
            const { useState } = React;

            function App() {
                const [file, setFile] = useState(null);
                const [loading, setLoading] = useState(false);
                const [analysis, setAnalysis] = useState(null);
                const [selectedRedactions, setSelectedRedactions] = useState([]);

                const handleFileUpload = async (e) => {
                    const uploadedFile = e.target.files[0];
                    if (!uploadedFile) return;
                    
                    setFile(uploadedFile);
                    setLoading(true);

                    const formData = new FormData();
                    formData.append('file', uploadedFile);

                    try {
                        const response = await fetch('/api/analyze', {
                            method: 'POST',
                            body: formData,
                        });
                        const data = await response.json();
                        setAnalysis(data);
                        setSelectedRedactions(data.suggested_redactions || []);
                    } catch (err) {
                        alert("Failed to analyze document.");
                    } finally {
                        setLoading(false);
                    }
                };

                const removeRedaction = (id) => {
                    setSelectedRedactions(selectedRedactions.filter(r => r.id !== id));
                };

                const handleExport = async () => {
                    if (!file) return;

                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('redactions_json', JSON.stringify(selectedRedactions));

                    try {
                        const response = await fetch('/api/redact-and-export', {
                            method: 'POST',
                            body: formData,
                        });

                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `sanitized_${file.name}`;
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                    } catch (err) {
                        alert("Export failed.");
                    }
                };

                return (
                    <div className="min-h-screen p-8">
                        <header className="flex items-center justify-between pb-6 border-b border-slate-800 mb-8">
                            <h1 className="text-2xl font-bold tracking-tight text-indigo-400">🛡️ AI Redaction Studio</h1>
                            {analysis && (
                                <button
                                    onClick={handleExport}
                                    className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-lg font-medium shadow-lg transition"
                                >
                                    Export Sanitized PDF
                                </button>
                            )}
                        </header>

                        {!analysis ? (
                            <div className="max-w-xl mx-auto mt-20 border-2 border-dashed border-slate-700 rounded-2xl p-12 text-center bg-slate-800/50">
                                <h3 className="text-lg font-semibold mb-2">Upload Document for Redaction</h3>
                                <p className="text-slate-400 text-sm mb-6">Supports PDF files and scanned records</p>
                                <input
                                    type="file"
                                    id="fileInput"
                                    className="hidden"
                                    onChange={handleFileUpload}
                                    accept=".pdf"
                                />
                                <label
                                    htmlFor="fileInput"
                                    className="cursor-pointer bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-lg font-medium inline-block shadow-md transition"
                                >
                                    {loading ? "Analyzing Document..." : "Select PDF File"}
                                </label>
                            </div>
                        ) : (
                            <div className="grid grid-cols-12 gap-8">
                                <div className="col-span-4 space-y-6">
                                    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                                        <h2 className="text-lg font-semibold mb-4 text-indigo-400">Extracted Metadata</h2>
                                        <div className="space-y-4 text-sm">
                                            <div>
                                                <span className="text-slate-400 block text-xs">Total Pages</span>
                                                <span className="font-semibold">{analysis.metadata.page_count}</span>
                                            </div>
                                            <div>
                                                <span className="text-slate-400 block text-xs">Parties Identified</span>
                                                <div className="flex flex-wrap gap-1 mt-1">
                                                    {analysis.metadata.parties_involved.map((party, idx) => (
                                                        <span key={idx} className="bg-slate-700 px-2.5 py-1 rounded-md text-xs">{party}</span>
                                                    ))}
                                                </div>
                                            </div>
                                            <div>
                                                <span className="text-slate-400 block text-xs">Key Dates</span>
                                                <div className="flex flex-wrap gap-1 mt-1">
                                                    {analysis.metadata.dates_mentioned.map((d, idx) => (
                                                        <span key={idx} className="bg-slate-700 px-2.5 py-1 rounded-md text-xs">{d}</span>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="col-span-8 bg-slate-800 rounded-xl p-6 border border-slate-700">
                                    <h2 className="text-lg font-semibold mb-6 text-indigo-400">
                                        Suggested Redactions ({selectedRedactions.length})
                                    </h2>

                                    <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                                        {selectedRedactions.map((item) => (
                                            <div
                                                key={item.id}
                                                className="flex items-center justify-between p-4 bg-slate-900/60 rounded-lg border border-slate-700/60"
                                            >
                                                <div className="space-y-1">
                                                    <div className="flex items-center gap-2">
                                                        <span className="bg-red-500/10 text-red-400 border border-red-500/20 text-xs px-2 py-0.5 rounded font-mono uppercase">
                                                            {item.type}
                                                        </span>
                                                        <span className="text-xs text-slate-400">Page {item.page + 1}</span>
                                                    </div>
                                                    <p className="font-mono text-sm text-slate-200">{item.text}</p>
                                                </div>

                                                <button
                                                    onClick={() => removeRedaction(item.id)}
                                                    className="px-3 py-1 bg-red-500/20 text-red-300 hover:bg-red-500/40 rounded-lg text-xs transition"
                                                >
                                                    Remove
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                );
            }

            ReactDOM.createRoot(document.getElementById('root')).render(<App />);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
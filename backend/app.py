from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flasgger import Swagger  # 1. Import Swagger
from utils import extract_text_from_pdf, validate_resume, clean_text, analyze_gap, generate_roadmap, generate_suggestions
from model import predict_roles

app = Flask(__name__)
CORS(app)

# 2. Initialize Swagger
swagger = Swagger(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze a Resume PDF
    ---
    tags:
      - Analysis
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The PDF resume to analyze.
    responses:
      200:
        description: Analysis results including roles, score, and roadmap.
      400:
        description: Invalid input or file format.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid Input - Only PDF files are allowed"}), 400
        
    # Read file stream
    file_stream = file.stream
        
    # Extract
    text = extract_text_from_pdf(file_stream)
    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"}), 400
        
    # Validate Resume
    if not validate_resume(text):
        return jsonify({"error": "Invalid Input – Not a Resume"}), 400
        
    # Process Text
    cleaned_txt = clean_text(text)
    
    # Predict Roles
    roles = predict_roles(cleaned_txt)
    top_role_name = roles[0]['name'] if roles else "Web Developer"
    
    # Gap Analysis
    match_score, missing_skills = analyze_gap(cleaned_txt, top_role_name)
    
    # Roadmap
    roadmap = generate_roadmap(missing_skills, top_role_name)
    
    # Suggestions
    suggestions = generate_suggestions(cleaned_txt)
    
    response = {
        "roles": roles,
        "match_score": match_score,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "suggestions": suggestions
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flasgger import Swagger  # 1. Import Swagger
from utils import extract_text_from_pdf, validate_resume, clean_text, analyze_gap, generate_roadmap, generate_suggestions
from model import predict_roles

app = Flask(__name__)
CORS(app)

# 2. Initialize Swagger
swagger = Swagger(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze a Resume PDF
    ---
    tags:
      - Analysis
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The PDF resume to analyze.
    responses:
      200:
        description: Analysis results including roles, score, and roadmap.
      400:
        description: Invalid input or file format.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid Input - Only PDF files are allowed"}), 400
        
    # Read file stream
    file_stream = file.stream
        
    # Extract
    text = extract_text_from_pdf(file_stream)
    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"}), 400
        
    # Validate Resume
    if not validate_resume(text):
        return jsonify({"error": "Invalid Input – Not a Resume"}), 400
        
    # Process Text
    cleaned_txt = clean_text(text)
    
    # Predict Roles
    roles = predict_roles(cleaned_txt)
    top_role_name = roles[0]['name'] if roles else "Web Developer"
    
    # Gap Analysis
    match_score, missing_skills = analyze_gap(cleaned_txt, top_role_name)
    
    # Roadmap
    roadmap = generate_roadmap(missing_skills, top_role_name)
    
    # Suggestions
    suggestions = generate_suggestions(cleaned_txt)
    
    response = {
        "roles": roles,
        "match_score": match_score,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "suggestions": suggestions
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

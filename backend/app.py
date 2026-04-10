from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flasgger import Swagger, swag_from
from utils import extract_text_from_pdf, validate_resume, clean_text, analyze_gap, generate_roadmap, generate_suggestions
from model import predict_roles

app = Flask(__name__)
CORS(app)

# Swagger Config
app.config['SWAGGER'] = {
    'title': 'Resume Analyzer API',
    'uiversion': 3
}

swagger = Swagger(app)

@app.route('/analyze', methods=['POST'])
@swag_from({
    'tags': ['Resume Analysis'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Upload resume PDF file'
        }
    ],
    'responses': {
        200: {
            'description': 'Analysis successful',
            'examples': {
                'application/json': {
                    "roles": [{"name": "Web Developer", "score": 0.85}],
                    "match_score": 75,
                    "missing_skills": ["Docker", "Kubernetes"],
                    "roadmap": ["Learn Docker", "Learn Kubernetes"],
                    "suggestions": ["Improve formatting"]
                }
            }
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid Input - Only PDF files are allowed"}), 400
        
    file_stream = file.stream
        
    text = extract_text_from_pdf(file_stream)
    if not text.strip():
        return jsonify({"error": "Could not extract text from PDF"}), 400
        
    if not validate_resume(text):
        return jsonify({"error": "Invalid Input – Not a Resume"}), 400
        
    cleaned_txt = clean_text(text)
    
    roles = predict_roles(cleaned_txt)
    top_role_name = roles[0]['name'] if roles else "Web Developer"
    
    match_score, missing_skills = analyze_gap(cleaned_txt, top_role_name)
    roadmap = generate_roadmap(missing_skills, top_role_name)
    suggestions = generate_suggestions(cleaned_txt)
    
    response = {
        "roles": roles,
        "match_score": match_score,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "suggestions": suggestions
    }
    
    return jsonify(response), 200


# ReDoc endpoint
@app.route('/redoc')
def redoc():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <title>ReDoc</title>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
      </head>
      <body>
        <redoc spec-url="/apispec_1.json"></redoc>
      </body>
    </html>
    """


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

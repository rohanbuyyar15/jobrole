from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
import os
from utils import extract_text_from_pdf, validate_resume, clean_text, analyze_gap, generate_roadmap, generate_suggestions
from model import predict_roles

app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"  # Swagger UI available at /docs
}

swagger_template = {
    "info": {
        "title": "Resume Analyzer API",
        "description": "API for analyzing resumes, predicting job roles, and generating career roadmaps",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@example.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)
@app.route('/')
def home():
    return jsonify({"message": "Resume AI API is running", "docs": "/docs"}), 200
    

@app.route('/analyze', methods=['POST'])
@swag_from({
    'tags': ['Resume Analysis'],
    'summary': 'Analyze a resume PDF',
    'description': 'Upload a PDF resume to get role predictions, skill gap analysis, career roadmap, and improvement suggestions.',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'PDF resume file to analyze'
        }
    ],
    'responses': {
        200: {
            'description': 'Successful analysis',
            'schema': {
                'type': 'object',
                'properties': {
                    'roles': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'example': 'Data Scientist'},
                                'confidence': {'type': 'number', 'example': 0.85}
                            }
                        },
                        'description': 'Predicted job roles with confidence scores'
                    },
                    'match_score': {
                        'type': 'number',
                        'example': 72.5,
                        'description': 'Percentage match with top predicted role'
                    },
                    'missing_skills': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['Docker', 'Kubernetes', 'AWS'],
                        'description': 'Skills missing for the top role'
                    },
                    'roadmap': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'step': {'type': 'integer'},
                                'skill': {'type': 'string'},
                                'resources': {'type': 'array', 'items': {'type': 'string'}}
                            }
                        },
                        'description': 'Learning roadmap to acquire missing skills'
                    },
                    'suggestions': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Resume improvement suggestions'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'No file uploaded'
                    }
                }
            }
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


@app.route('/health', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'Health check endpoint',
    'description': 'Check if the API is running',
    'responses': {
        200: {
            'description': 'API is healthy',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'healthy'},
                    'version': {'type': 'string', 'example': '1.0.0'}
                }
            }
        }
    }
})
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

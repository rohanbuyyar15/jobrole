// NOTE: When deploying your backend to Render, update this URL to your Render deployment URL.
// Example: const API_BASE_URL = 'https://my-resume-backend.onrender.com';
const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000' : 'https://YOUR-RENDER-BACKEND-URL.onrender.com';

async function analyzeResume() {
    const textStr = document.getElementById('resumeText').value;
    const errorDiv = document.getElementById('error-msg');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    // Reset states
    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    
    if(!textStr.trim()) {
        errorDiv.textContent = "Please paste your resume text first.";
        errorDiv.classList.remove('hidden');
        return;
    }
    
    loadingDiv.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resume: textStr })
        });
        
        const data = await response.json();
        
        // 1. INPUT VALIDATION handling (Check Invalid Input)
        if (data.error) {
            errorDiv.textContent = data.error;
            errorDiv.classList.remove('hidden');
        } else {
            // 10. OUTPUT FORMAT
            displayResults(data);
            resultsDiv.classList.remove('hidden');
        }
    } catch (err) {
        errorDiv.textContent = "An error occurred while communicating with the server.";
        errorDiv.classList.remove('hidden');
    } finally {
        loadingDiv.classList.add('hidden');
    }
}

function displayResults(data) {
    // Top 3 roles
    const rolesList = document.getElementById('rolesList');
    rolesList.innerHTML = '';
    data.predictions.forEach((pred, i) => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="rank">#${i+1}</span> <strong>${pred.role}</strong> - ${pred.confidence}% confidence`;
        rolesList.appendChild(li);
    });
    
    // Match Score
    document.getElementById('matchScore').textContent = data.match_score;
    document.getElementById('scoreRoleText').textContent = `Matched against required skills for ${data.predictions[0].role}`;
    
    // Section Analysis
    const sectionsList = document.getElementById('sectionsList');
    sectionsList.innerHTML = '';
    for(const [sec, grade] of Object.entries(data.sections)) {
        const li = document.createElement('li');
        const badgeClass = grade.toLowerCase();
        li.innerHTML = `<strong>${sec}:</strong> <span class="badge ${badgeClass}">${grade}</span>`;
        sectionsList.appendChild(li);
    }
    
    // Gap Analysis (Missing Skills)
    const missingSkillsTags = document.getElementById('missingSkillsTags');
    missingSkillsTags.innerHTML = '';
    if(data.missing_skills.length === 0) {
        missingSkillsTags.innerHTML = '<em>None identified! Great match!</em>';
    } else {
        data.missing_skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'tag missing';
            span.textContent = skill;
            missingSkillsTags.appendChild(span);
        });
    }
    
    // Resume Suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    data.suggestions.forEach(sug => {
        const li = document.createElement('li');
        li.textContent = sug;
        suggestionsList.appendChild(li);
    });
    
    // Roadmap Generation
    const roadmapList = document.getElementById('roadmapList');
    roadmapList.innerHTML = '';
    data.roadmap.forEach(step => {
        const li = document.createElement('li');
        li.textContent = step;
        roadmapList.appendChild(li);
    });
}

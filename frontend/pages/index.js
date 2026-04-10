import { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
  };

  const handleChange = (e) => {
    handleFile(e.target.files[0]);
  };

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Invalid file format. Please upload a PDF resume.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

    try {
      const res = await axios.post(`${apiUrl}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (typeof window !== 'undefined') {
        localStorage.setItem('resumeResult', JSON.stringify(res.data));
        router.push('/result');
      }
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.error || 'Failed to analyze resume. Make sure backend is running.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-panel p-8 w-full max-w-2xl text-center shadow-2xl">
        <h1 className="text-4xl font-extrabold mb-4 text-white drop-shadow-md">AI Resume Analyzer</h1>
        <p className="text-gray-200 mb-8 font-medium">Upload your resume to predict your job role and get customized improvement suggestions.</p>

        <div 
          className={`border-2 border-dashed rounded-2xl p-10 transition-all duration-300 ${file ? 'border-green-400 bg-white/10 scale-[1.02]' : 'border-gray-300 hover:border-white hover:bg-white/5'}`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input 
            type="file" 
            accept="application/pdf" 
            className="hidden" 
            id="fileUpload" 
            onChange={handleChange}
          />
          <label htmlFor="fileUpload" className="cursor-pointer flex flex-col items-center">
            <svg className={`w-16 h-16 mb-4 transition-colors ${file ? 'text-green-400' : 'text-gray-300'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            <span className="text-xl font-bold mb-1">{file ? file.name : "Drag & Drop your PDF here"}</span>
            <span className="text-sm font-semibold text-gray-300">or click to browse files</span>
          </label>
        </div>

        {error && <div className="mt-6 text-red-500 font-bold bg-white p-3 rounded-lg shadow-md animate-pulse">{error}</div>}

        <button 
          onClick={handleUpload} 
          disabled={loading || !file}
          className="mt-8 w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-xl transition-all shadow-xl hover:shadow-2xl text-lg flex justify-center items-center transform hover:-translate-y-1"
        >
          {loading ? (
            <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : "Analyze Resume"}
        </button>
      </div>
    </div>
  );
}

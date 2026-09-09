import React, { useState } from 'react';
import axios from 'axios';
import { 
  Upload, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Target, 
  BookOpen, 
  HelpCircle,
  Loader2,
  User,
  Mail,
  Phone
} from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a candidate resume PDF.');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please provide a target job description.');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/analyze`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      console.log('Backend response payload:', response.data);
      setResult(response.data);
    } catch (err: any) {
      console.error('Request error:', err);
      setError(
        err.response?.data?.detail || 'Analysis request failed. Please check backend status.'
      );
    } finally {
      setLoading(false);
    }
  };

  // Direct backend payload field mappings
  const totalScore = Math.round(result?.scores?.overall_ats_score ?? 0);
  const semanticScore = Math.round(result?.scores?.semantic_similarity_score ?? 0);
  const keywordScore = Math.round(result?.scores?.skill_match_score ?? 0);

  const matchingSkills: string[] = result?.skills?.matching_skills ?? [];
  const missingSkills: string[] = result?.skills?.missing_skills ?? [];
  const extractedSkills: string[] = result?.skills?.all_extracted_skills ?? [];

  const summary: string = result?.summary ?? 'Analysis completed successfully.';
  const strengths: string[] = result?.strengths ?? [];
  const weaknesses: string[] = result?.weaknesses ?? [];
  const suggestions: string[] = result?.actionable_suggestions ?? [];

  const techQuestions: string[] = result?.interview_questions?.technical ?? [];
  const projectQuestions: string[] = result?.interview_questions?.project_based ?? [];
  const behavioralQuestions: string[] = result?.interview_questions?.behavioral ?? [];

  const contactInfo = result?.contact_info;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="border-b border-slate-800 pb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
              <Sparkles className="text-cyan-400 h-8 w-8" />
              AI Resume Intelligence Engine
            </h1>
            <p className="text-slate-400 mt-1 text-sm">
              Vector semantic ATS scoring, technical keyword extraction, and automated recruiter feedback
            </p>
          </div>
          <div className="text-xs font-mono bg-cyan-950/60 border border-cyan-800 text-cyan-300 px-3 py-1.5 rounded-md">
            Production Live
          </div>
        </header>

        {/* Candidate Meta Header (when parsed) */}
        {contactInfo && (contactInfo.name || contactInfo.email) && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center gap-6 text-sm text-slate-300">
            {contactInfo.name && (
              <span className="flex items-center gap-2 font-medium text-white">
                <User className="h-4 w-4 text-cyan-400" /> {contactInfo.name}
              </span>
            )}
            {contactInfo.email && (
              <span className="flex items-center gap-2 text-slate-400">
                <Mail className="h-4 w-4 text-slate-500" /> {contactInfo.email}
              </span>
            )}
            {contactInfo.phone && (
              <span className="flex items-center gap-2 text-slate-400">
                <Phone className="h-4 w-4 text-slate-500" /> {contactInfo.phone}
              </span>
            )}
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleAnalyze} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                1. Upload Candidate Resume (PDF)
              </label>
              <div className="border-2 border-dashed border-slate-700 hover:border-cyan-500/50 transition-colors rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer relative">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <Upload className="h-10 w-10 text-slate-500 mb-3" />
                <p className="text-sm font-medium text-slate-200">
                  {file ? file.name : 'Click or drag PDF here'}
                </p>
                <p className="text-xs text-slate-500 mt-1">Maximum size: 5MB</p>
              </div>
            </div>
            {file && (
              <div className="mt-4 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/30 border border-emerald-800/40 p-2.5 rounded-md">
                <FileText className="h-4 w-4" /> Selected: {file.name}
              </div>
            )}
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                2. Target Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste role requirements, core technologies, and expectations..."
                rows={5}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:opacity-50 text-white font-medium py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 transition-all cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Processing ATS Vectors...
                </>
              ) : (
                'Run Evaluation'
              )}
            </button>
          </div>
        </form>

        {/* Error Notification */}
        {error && (
          <div className="bg-red-950/40 border border-red-800/50 p-4 rounded-xl flex items-center gap-3 text-red-300 text-sm">
            <AlertCircle className="h-5 w-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Results View */}
        {result && (
          <div className="space-y-6">
            {/* Score Metric Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Composite Match
                </span>
                <div className="text-5xl font-extrabold text-cyan-400 mt-2">
                  {totalScore}%
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
                  <div
                    className="bg-cyan-400 h-full transition-all duration-700"
                    style={{ width: `${Math.min(100, Math.max(0, totalScore))}%` }}
                  />
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Semantic Overlap
                </span>
                <div className="text-4xl font-bold text-blue-400 mt-2">
                  {semanticScore}%
                </div>
                <p className="text-xs text-slate-500 mt-2">Dense Vector Space Cosine Similarity</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Keyword Direct Match
                </span>
                <div className="text-4xl font-bold text-indigo-400 mt-2">
                  {keywordScore}%
                </div>
                <p className="text-xs text-slate-500 mt-2">Technical Lexicon Intersection</p>
              </div>
            </div>

            {/* Skills Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-sm font-semibold text-emerald-400 flex items-center gap-2 mb-4">
                  <CheckCircle2 className="h-4 w-4" /> Verified Target Competencies
                </h3>
                <div className="flex flex-wrap gap-2">
                  {matchingSkills.length > 0 ? (
                    matchingSkills.map((skill: string, idx: number) => (
                      <span
                        key={idx}
                        className="bg-emerald-950/50 border border-emerald-800/50 text-emerald-300 text-xs px-2.5 py-1 rounded-md"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">No overlapping technical skills detected.</span>
                  )}
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-sm font-semibold text-amber-400 flex items-center gap-2 mb-4">
                  <Target className="h-4 w-4" /> Stack Development Gaps
                </h3>
                <div className="flex flex-wrap gap-2">
                  {missingSkills.length > 0 ? (
                    missingSkills.map((skill: string, idx: number) => (
                      <span
                        key={idx}
                        className="bg-amber-950/50 border border-amber-800/50 text-amber-300 text-xs px-2.5 py-1 rounded-md"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-500">All required target competencies satisfied.</span>
                  )}
                </div>
              </div>
            </div>

            {/* Extracted Profile Skills (if available) */}
            {extractedSkills.length > 0 && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">All Identified Candidate Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {extractedSkills.map((sk: string, idx: number) => (
                    <span
                      key={idx}
                      className="bg-slate-950 border border-slate-800 text-slate-300 text-xs px-2.5 py-1 rounded-md"
                    >
                      {sk}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* AI Executive Overview & Suggestions */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2 mb-2">
                  <BookOpen className="h-4 w-4 text-cyan-400" /> Executive Overview
                </h3>
                <p className="text-sm text-slate-300 leading-relaxed bg-slate-950/50 border border-slate-800/60 p-4 rounded-lg">
                  {summary}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Key Profile Strengths</h4>
                  <ul className="space-y-2">
                    {strengths.map((st: string, i: number) => (
                      <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                        <span className="text-emerald-400 font-bold">•</span>
                        <span>{st}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Actionable Enhancements</h4>
                  <ul className="space-y-2">
                    {(suggestions.length > 0 ? suggestions : weaknesses).map((sug: string, i: number) => (
                      <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                        <span className="text-cyan-400 font-bold">•</span>
                        <span>{sug}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Targeted Recruiter Prompts */}
            {(techQuestions.length > 0 || projectQuestions.length > 0 || behavioralQuestions.length > 0) && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2 mb-4">
                  <HelpCircle className="h-4 w-4 text-blue-400" /> Targeted Recruiter Interview Prompts
                </h3>
                <div className="space-y-4">
                  {techQuestions.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-slate-400 block mb-1.5">
                        Technical & Architectural Deep-Dives:
                      </span>
                      <ul className="space-y-1.5">
                        {techQuestions.map((q: string, i: number) => (
                          <li key={i} className="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                            {q}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {projectQuestions.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-slate-400 block mb-1.5">
                        Project Experience & Scaling:
                      </span>
                      <ul className="space-y-1.5">
                        {projectQuestions.map((q: string, i: number) => (
                          <li key={i} className="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                            {q}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {behavioralQuestions.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-slate-400 block mb-1.5">
                        Behavioral & Workflow Dynamics:
                      </span>
                      <ul className="space-y-1.5">
                        {behavioralQuestions.map((q: string, i: number) => (
                          <li key={i} className="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                            {q}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
// document.addEventListener('DOMContentLoaded', () => {
//   setupTabs();
//   setupFileUploadHandlers();
//   setupEventListeners();
// });

// function setupTabs() {
//   const tabs = document.querySelectorAll('.nav-tab');
//   const contents = document.querySelectorAll('.tab-content');
//   const cards = document.querySelectorAll('.dashboard-card');

//   tabs.forEach(tab => {
//     tab.addEventListener('click', () => {
//       tabs.forEach(t => t.classList.remove('active'));
//       tab.classList.add('active');
//       contents.forEach(c => c.classList.remove('active'));
//       document.getElementById(tab.dataset.tab).classList.add('active');
//     });
//   });

//   cards.forEach(card => {
//     card.addEventListener('click', () => {
//       const target = card.dataset.action;
//       document.querySelector(`.nav-tab[data-tab="${target}"]`).click();
//     });
//   });
// }

// function setupFileUploadHandlers() {
//   const resumeUpload = document.getElementById('resume-upload');
//   const resumeFileInput = document.getElementById('resume-file');
//   const resumeFileInfo = document.getElementById('resume-file-info');

//   resumeUpload.addEventListener('click', () => resumeFileInput.click());

//   resumeFileInput.addEventListener('change', () => {
//     if (resumeFileInput.files.length > 0) {
//       const file = resumeFileInput.files[0];
//       resumeFileInfo.classList.remove('hidden');
//       resumeFileInfo.querySelector('.file-name').textContent = file.name;
//     }
//   });

//   resumeFileInfo.querySelector('.remove-file').addEventListener('click', () => {
//     resumeFileInput.value = '';
//     resumeFileInfo.classList.add('hidden');
//   });
// }

// function setupEventListeners() {
//   document.getElementById('analyze-resume').addEventListener('click', analyzeResume);
//   document.getElementById('analyze-interview').addEventListener('click', analyzeInterview); // ✅ Added this
// }

// // ======================
// // 🔍 Analyze Resume Logic
// // ======================

// function analyzeResume() {
//   const resumeFile = document.getElementById('resume-file').files[0];
//   const jobDescription = document.getElementById('job-description').value;

//   if (!resumeFile || !jobDescription.trim()) {
//     alert('Please upload a resume and enter a job description.');
//     return;
//   }

//   showLoadingModal();
//   startProgressBar('analysis-progress', 'progress-text');

//   const formData = new FormData();
//   formData.append('resume', resumeFile);
//   formData.append('job_description', jobDescription);

//   fetch('http://127.0.0.1:5000/analyze-resume', {
//     method: 'POST',
//     body: formData,
//   })
//     .then(res => res.json())
//     .then(data => {
//       hideLoadingModal();
//       displayResumeResults(data);
//     })
//     .catch(error => {
//       hideLoadingModal();
//       alert('Error analyzing resume. Make sure backend is running.');
//       console.error(error);
//     });
// }

// // ==========================
// // 📊 Display Resume Results
// // ==========================

// function displayResumeResults(data) {
//   const resultsSection = document.getElementById('resume-results');

//   document.getElementById('similarity-score').textContent = data.similarity_score || 0;

//   const matchedSkills = document.getElementById('matched-skills');
//   matchedSkills.innerHTML = '';
//   (data.matched_skills || []).forEach(skill => {
//     const tag = document.createElement('span');
//     tag.className = 'skill-tag';
//     tag.textContent = skill;
//     matchedSkills.appendChild(tag);
//   });

//   const missingSkills = document.getElementById('missing-skills');
//   missingSkills.innerHTML = '';
//   (data.missing_skills || []).forEach(skill => {
//     const tag = document.createElement('span');
//     tag.className = 'skill-tag missing';
//     tag.textContent = skill;
//     missingSkills.appendChild(tag);
//   });

//   const improvementList = document.getElementById('improvement-suggestions');
//   improvementList.innerHTML = '';
//   (data.improvement_areas || []).forEach(point => {
//     const li = document.createElement('li');
//     li.textContent = point;
//     improvementList.appendChild(li);
//   });

//   resultsSection.classList.remove('hidden');
// }

// // ======================
// // 💡 Utility Functions
// // ======================

// function showLoadingModal() {
//   document.getElementById('loading-modal').classList.remove('hidden');
// }

// function hideLoadingModal() {
//   document.getElementById('loading-modal').classList.add('hidden');
// }

// function startProgressBar(progressId, textId) {
//   const progressBar = document.getElementById(progressId);
//   const progressText = document.getElementById(textId);
//   let width = 0;
//   const interval = setInterval(() => {
//     if (width >= 100) {
//       clearInterval(interval);
//     } else {
//       width += 1;
//       progressBar.style.width = `${width}%`;
//       progressText.textContent = `${width}% complete`;
//     }
//   }, 15);
// }

// // ==============================
// // 🎥 Analyze Interview Placeholder
// // ==============================

// function analyzeInterview() {
//   const interviewFile = document.getElementById('interview-file').files[0];

//   if (!interviewFile) {
//     alert('Please upload an interview recording.');
//     return;
//   }

//   showLoadingModal();
//   startProgressBar('interview-progress', 'interview-progress-text');

//   const formData = new FormData();
//   formData.append('interview', interviewFile);

//   fetch('http://127.0.0.1:5000/analyze-interview', {
//     method: 'POST',
//     body: formData
//   })
//     .then(res => res.json())
//     .then(data => {
//       hideLoadingModal();
//       displayInterviewResults(data); // TODO: Implement this function next
//     })
//     .catch(error => {
//       hideLoadingModal();
//       alert('Error during interview analysis.');
//       console.error('Interview analysis error:', error);
//     });
// }




// function displayInterviewResults(data) {
//   const resultSection = document.getElementById('interview-results');

//   // Score Displays
//   document.getElementById('confidence-score').textContent = data.confidence_score + "%";
//   document.getElementById('clarity-score').textContent = data.clarity_score + "%";
//   document.getElementById('hesitation-rate').textContent = data.hesitation_rate + "%";

//   // Emotion Chart (optional placeholder for pie chart or bar chart)
//   const emotionList = document.getElementById('emotion-breakdown');
//   emotionList.innerHTML = '';
//   for (const [emotion, value] of Object.entries(data.emotion_data)) {
//     const li = document.createElement('li');
//     li.textContent = `${emotion}: ${value}%`;
//     emotionList.appendChild(li);
//   }

//   // Feedback Suggestions
//   const feedbackList = document.getElementById('interview-feedback');
//   feedbackList.innerHTML = '';
//   data.feedback.forEach(item => {
//     const li = document.createElement('li');
//     li.textContent = item;
//     feedbackList.appendChild(li);
//   });

//   resultSection.classList.remove('hidden');
// }

































































document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  setupFileUploadHandlers();
  setupEventListeners();
  loadAnalyticsDashboard();
});

function setupTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  const contents = document.querySelectorAll('.tab-content');
  const cards = document.querySelectorAll('.dashboard-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      contents.forEach(c => c.classList.remove('active'));
      document.getElementById(tab.dataset.tab).classList.add('active');
      
      // Load analytics when results tab is selected
      if (tab.dataset.tab === 'results') {
        loadAnalyticsDashboard();
      }
    });
  });

  cards.forEach(card => {
    card.addEventListener('click', () => {
      const target = card.dataset.action;
      document.querySelector(`.nav-tab[data-tab="${target}"]`).click();
    });
  });
}

function setupFileUploadHandlers() {
  // Resume upload handler
  const resumeUpload = document.getElementById('resume-upload');
  const resumeFileInput = document.getElementById('resume-file');
  const resumeFileInfo = document.getElementById('resume-file-info');

  resumeUpload.addEventListener('click', () => resumeFileInput.click());

  resumeFileInput.addEventListener('change', () => {
    if (resumeFileInput.files.length > 0) {
      const file = resumeFileInput.files[0];
      resumeFileInfo.classList.remove('hidden');
      resumeFileInfo.querySelector('.file-name').textContent = file.name;
    }
  });

  resumeFileInfo.querySelector('.remove-file').addEventListener('click', () => {
    resumeFileInput.value = '';
    resumeFileInfo.classList.add('hidden');
  });

  // Interview upload handler (supports both audio and video)
  const interviewUpload = document.getElementById('interview-upload');
  const interviewFileInput = document.getElementById('interview-file');
  const interviewFileInfo = document.getElementById('interview-file-info');

  if (interviewUpload && interviewFileInput && interviewFileInfo) {
    interviewUpload.addEventListener('click', () => interviewFileInput.click());

    interviewFileInput.addEventListener('change', () => {
      if (interviewFileInput.files.length > 0) {
        const file = interviewFileInput.files[0];
        const fileType = getFileType(file.name);
        
        interviewFileInfo.classList.remove('hidden');
        interviewFileInfo.querySelector('.file-name').textContent = file.name;
        
        // Add file type badge
        const typeBadge = interviewFileInfo.querySelector('.file-type-badge');
        typeBadge.textContent = fileType === 'video' ? '📹 Video' : '🎵 Audio';
        typeBadge.className = `file-type-badge ${fileType}`;
      }
    });

    interviewFileInfo.querySelector('.remove-file').addEventListener('click', () => {
      interviewFileInput.value = '';
      interviewFileInfo.classList.add('hidden');
    });

    // Drag and drop functionality
    interviewUpload.addEventListener('dragover', (e) => {
      e.preventDefault();
      interviewUpload.classList.add('drag-over');
    });

    interviewUpload.addEventListener('dragleave', () => {
      interviewUpload.classList.remove('drag-over');
    });

    interviewUpload.addEventListener('drop', (e) => {
      e.preventDefault();
      interviewUpload.classList.remove('drag-over');
      
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        interviewFileInput.files = files;
        interviewFileInput.dispatchEvent(new Event('change'));
      }
    });
  }
}

function setupEventListeners() {
  document.getElementById('analyze-resume').addEventListener('click', analyzeResume);
  document.getElementById('analyze-interview').addEventListener('click', analyzeInterview);
  document.getElementById('download-report').addEventListener('click', downloadResumeReport);
  
  // Add event listener for interview download (will be added when results are shown)
  document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'download-interview-report') {
      downloadInterviewReport();
    }
  });
}

// =======================================
// 🎬 Video/Audio File Type Detection
// =======================================

function getFileType(filename) {
  const extension = filename.toLowerCase().split('.').pop();
  const videoFormats = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v'];
  const audioFormats = ['mp3', 'wav', 'm4a', 'aac', 'ogg'];
  
  if (videoFormats.includes(extension)) {
    return 'video';
  } else if (audioFormats.includes(extension)) {
    return 'audio';
  } else {
    return 'unknown';
  }
}

function getFileIcon(filename) {
  const fileType = getFileType(filename);
  return fileType === 'video' ? '📹' : '🎵';
}

function displayVideoMetadata(data, container) {
  const metadata = data.video_metadata || {};
  const processingInfo = data.processing_info || {};
  
  // Remove existing metadata display
  const existingMetadata = container.querySelector('.video-metadata');
  if (existingMetadata) {
    existingMetadata.remove();
  }
  
  // Create metadata section
  const metadataSection = document.createElement('div');
  metadataSection.className = 'video-metadata';
  
  const fileType = metadata.file_type || processingInfo.file_type || 'unknown';
  const isVideo = fileType === 'video';
  
  metadataSection.innerHTML = `
    <h5>${isVideo ? '📹' : '🎵'} ${isVideo ? 'Video' : 'Audio'} File Information</h5>
    ${processingInfo.original_filename ? `
      <div class="metadata-item">
        <span class="metadata-label">Original File:</span>
        <span class="metadata-value">${processingInfo.original_filename}</span>
      </div>
    ` : ''}
    ${metadata.original_format ? `
      <div class="metadata-item">
        <span class="metadata-label">Format:</span>
        <span class="metadata-value">${metadata.original_format.toUpperCase()}</span>
      </div>
    ` : ''}
    ${metadata.duration ? `
      <div class="metadata-item">
        <span class="metadata-label">Duration:</span>
        <span class="metadata-value">${formatDuration(metadata.duration)}</span>
      </div>
    ` : ''}
    ${metadata.resolution && isVideo ? `
      <div class="metadata-item">
        <span class="metadata-label">Resolution:</span>
        <span class="metadata-value">${metadata.resolution[0]} × ${metadata.resolution[1]}</span>
      </div>
    ` : ''}
    ${metadata.fps && isVideo ? `
      <div class="metadata-item">
        <span class="metadata-label">Frame Rate:</span>
        <span class="metadata-value">${metadata.fps} FPS</span>
      </div>
    ` : ''}
    ${metadata.audio_extracted ? `
      <div class="metadata-item">
        <span class="metadata-label">Audio Extraction:</span>
        <span class="metadata-value">✅ Successful</span>
      </div>
    ` : ''}
  `;
  
  // Insert metadata after the main results
  const feedbackSection = container.querySelector('#interview-feedback').parentElement;
  feedbackSection.parentElement.insertBefore(metadataSection, feedbackSection.nextSibling);
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// ======================
// 🔍 Analyze Resume Logic
// ======================

function analyzeResume() {
  const resumeFile = document.getElementById('resume-file').files[0];
  const jobDescription = document.getElementById('job-description').value;

  if (!resumeFile || !jobDescription.trim()) {
    alert('Please upload a resume and enter a job description.');
    return;
  }

  showLoadingModal();
  startProgressBar('analysis-progress', 'progress-text');

  const userLevel = document.getElementById('user-level').value;

  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('job_description', jobDescription);
  formData.append('user_level', userLevel);

  fetch('http://127.0.0.1:5000/analyze-resume', {
    method: 'POST',
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      hideLoadingModal();
      displayResumeResults(data);
      saveAnalysisToLocalStorage('resume', data);
    })
    .catch(error => {
      hideLoadingModal();
      alert('Error analyzing resume. Make sure backend is running.');
      console.error(error);
    });
}

// ==========================
// 📊 Display Resume Results
// ==========================

function displayResumeResults(data) {
  const resultsSection = document.getElementById('resume-results');

  document.getElementById('similarity-score').textContent = data.similarity_score || 0;

  const matchedSkills = document.getElementById('matched-skills');
  matchedSkills.innerHTML = '';
  (data.matched_skills || []).forEach(skill => {
    const tag = document.createElement('span');
    tag.className = 'skill-tag';
    tag.textContent = skill;
    matchedSkills.appendChild(tag);
  });

  const missingSkills = document.getElementById('missing-skills');
  missingSkills.innerHTML = '';
  (data.missing_skills || []).forEach(skill => {
    const tag = document.createElement('span');
    tag.className = 'skill-tag missing';
    tag.textContent = skill;
    missingSkills.appendChild(tag);
  });

  const improvementList = document.getElementById('improvement-suggestions');
  improvementList.innerHTML = '';
  (data.improvement_areas || []).forEach(point => {
    const li = document.createElement('li');
    li.textContent = point;
    improvementList.appendChild(li);
  });

  // Add AI feedback if available
  if (data.ai_feedback) {
    displayAIFeedback(data.ai_feedback, 'resume');
  }

  // Add course recommendations if available
  if (data.learning_recommendations) {
    displayCourseRecommendations(data.learning_recommendations);
  }

  // Add career insights if available
  if (data.career_insights) {
    displayCareerInsights(data.career_insights);
  }

  resultsSection.classList.remove('hidden');
}

// ==============================
// 🎥 Analyze Interview Logic
// ==============================

function analyzeInterview() {
  const interviewFile = document.getElementById('interview-file').files[0];

  if (!interviewFile) {
    alert('Please upload an interview recording or video.');
    return;
  }

  const fileType = getFileType(interviewFile.name);
  const fileIcon = getFileIcon(interviewFile.name);
  
  // Validate file type
  if (fileType === 'unknown') {
    alert('Unsupported file format. Please upload MP4, AVI, MOV, MP3, WAV, or M4A files.');
    return;
  }

  showLoadingModal();
  
  // Update progress message based on file type
  const progressText = document.getElementById('interview-progress-text');
  if (fileType === 'video') {
    progressText.textContent = 'Processing video file...';
    setTimeout(() => {
      progressText.textContent = 'Extracting audio from video...';
    }, 2000);
    setTimeout(() => {
      progressText.textContent = 'Analyzing speech patterns...';
    }, 4000);
  } else {
    progressText.textContent = 'Processing audio file...';
  }
  
  startProgressBar('interview-progress', 'interview-progress-text');

  const formData = new FormData();
  formData.append('interview', interviewFile);

  console.log(`${fileIcon} Processing ${fileType} file: ${interviewFile.name}`);

  fetch('http://127.0.0.1:5000/analyze-interview', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      hideLoadingModal();
      
      if (data.error) {
        alert(`Analysis failed: ${data.error}`);
        return;
      }
      
      console.log('✅ Interview analysis completed:', data);
      displayInterviewResults(data);
      saveAnalysisToLocalStorage('interview', data);
    })
    .catch(error => {
      hideLoadingModal();
      alert(`Error during ${fileType} analysis. Make sure backend is running.`);
      console.error('Interview analysis error:', error);
    });
}

// ============================
// 🎯 Display Interview Results
// ============================

function displayInterviewResults(data) {
  const resultSection = document.getElementById('interview-results');
  
  // Store data for download
  currentInterviewData = data;

  // Update basic metrics
  document.getElementById('confidence-score').textContent = `${data.speech_analysis?.confidence_score || data.overall_score || 0}%`;
  document.getElementById('clarity-score').textContent = `${data.speech_analysis?.clarity_score || 0}%`;
  document.getElementById('hesitation-rate').textContent = `${data.speech_analysis?.hesitation_rate || 0}%`;

  // Emotion breakdown
  const emotionList = document.getElementById('emotion-breakdown');
  emotionList.innerHTML = '';
  
  const emotions = data.sentiment_analysis?.emotion_breakdown || data.emotion_data || {};
  for (const [emotion, percent] of Object.entries(emotions)) {
    const li = document.createElement('li');
    li.textContent = `${emotion}: ${percent}%`;
    emotionList.appendChild(li);
  }

  // Feedback
  const feedbackList = document.getElementById('interview-feedback');
  feedbackList.innerHTML = '';
  const feedback = data.feedback || data.performance_summary?.recommendations || [];
  feedback.forEach(point => {
    const li = document.createElement('li');
    li.textContent = point;
    feedbackList.appendChild(li);
  });

  // Add AI feedback if available
  if (data.ai_feedback) {
    displayAIFeedback(data.ai_feedback, 'interview');
  }

  // Add video metadata if available
  if (data.video_metadata || data.processing_info) {
    displayVideoMetadata(data, resultSection);
  }

  resultSection.classList.remove('hidden');
}

// =======================================
// 🤖 Display AI-Powered Feedback
// =======================================

function displayAIFeedback(aiFeedback, type) {
  // Create AI feedback section
  const targetSection = type === 'resume' ? 
    document.querySelector('#resume-results .card__body') : 
    document.querySelector('#interview-results .card__body');
  
  let aiSection = document.getElementById(`ai-feedback-${type}`);
  
  if (!aiSection) {
    aiSection = document.createElement('div');
    aiSection.id = `ai-feedback-${type}`;
    aiSection.className = 'ai-feedback-section';
    aiSection.innerHTML = `
      <div class="ai-header">
        <h4>🤖 AI-Powered Insights ${aiFeedback.ai_powered ? '<span class="ai-badge">Powered by Gemini</span>' : '<span class="demo-badge">Demo Mode</span>'}</h4>
      </div>
      <div id="ai-content-${type}" class="ai-content"></div>
    `;
    targetSection.appendChild(aiSection);
  }

  const aiContent = document.getElementById(`ai-content-${type}`);
  aiContent.innerHTML = '';

  if (type === 'resume') {
    displayResumeAIFeedback(aiFeedback, aiContent);
  } else if (type === 'interview') {
    displayInterviewAIFeedback(aiFeedback, aiContent);
  }
}

function displayResumeAIFeedback(feedback, container) {
  const sections = [
    { key: 'overall_assessment', title: '📋 Overall Assessment', type: 'text' },
    { key: 'strengths', title: '💪 Key Strengths', type: 'list' },
    { key: 'critical_gaps', title: '🎯 Critical Gaps', type: 'list' },
    { key: 'optimization_tips', title: '🔧 Optimization Tips', type: 'list' },
    { key: 'industry_advice', title: '🏢 Industry Insights', type: 'list' },
    { key: 'next_steps', title: '🚀 Next Steps', type: 'list' }
  ];

  sections.forEach(section => {
    if (feedback[section.key]) {
      const sectionDiv = document.createElement('div');
      sectionDiv.className = 'ai-feedback-section';
      
      const title = document.createElement('h5');
      title.textContent = section.title;
      title.className = 'ai-section-title';
      sectionDiv.appendChild(title);

      if (section.type === 'text') {
        const text = document.createElement('p');
        text.textContent = feedback[section.key];
        text.className = 'ai-text-content';
        sectionDiv.appendChild(text);
      } else if (section.type === 'list' && Array.isArray(feedback[section.key])) {
        const list = document.createElement('ul');
        list.className = 'ai-list-content';
        feedback[section.key].forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          list.appendChild(li);
        });
        sectionDiv.appendChild(list);
      }

      container.appendChild(sectionDiv);
    }
  });
}

function displayInterviewAIFeedback(feedback, container) {
  const sections = [
    { key: 'performance_summary', title: '📊 Performance Summary', type: 'text' },
    { key: 'communication_strengths', title: '🗣️ Communication Strengths', type: 'list' },
    { key: 'areas_for_improvement', title: '📈 Areas for Improvement', type: 'list' },
    { key: 'technical_response_quality', title: '🔧 Technical Assessment', type: 'text' },
    { key: 'soft_skills_assessment', title: '🤝 Soft Skills Assessment', type: 'text' },
    { key: 'interview_strategies', title: '💡 Interview Strategies', type: 'list' },
    { key: 'practice_recommendations', title: '🎯 Practice Recommendations', type: 'list' }
  ];

  sections.forEach(section => {
    if (feedback[section.key]) {
      const sectionDiv = document.createElement('div');
      sectionDiv.className = 'ai-feedback-section';
      
      const title = document.createElement('h5');
      title.textContent = section.title;
      title.className = 'ai-section-title';
      sectionDiv.appendChild(title);

      if (section.type === 'text') {
        const text = document.createElement('p');
        text.textContent = feedback[section.key];
        text.className = 'ai-text-content';
        sectionDiv.appendChild(text);
      } else if (section.type === 'list' && Array.isArray(feedback[section.key])) {
        const list = document.createElement('ul');
        list.className = 'ai-list-content';
        feedback[section.key].forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          list.appendChild(li);
        });
        sectionDiv.appendChild(list);
      }

      container.appendChild(sectionDiv);
    }
  });
}

function displayCareerInsights(insights) {
  // Add career insights after course recommendations
  const courseSection = document.getElementById('course-recommendations');
  let insightsSection = document.getElementById('career-insights');
  
  if (!insightsSection) {
    insightsSection = document.createElement('div');
    insightsSection.id = 'career-insights';
    insightsSection.className = 'career-insights-section';
    insightsSection.innerHTML = `
      <h4>🎯 Career Development Insights ${insights.ai_powered ? '<span class="ai-badge">AI-Powered</span>' : ''}</h4>
      <div id="insights-content"></div>
    `;
    if (courseSection) {
      courseSection.parentNode.insertBefore(insightsSection, courseSection.nextSibling);
    } else {
      document.querySelector('#resume-results .card__body').appendChild(insightsSection);
    }
  }

  const insightsContent = document.getElementById('insights-content');
  insightsContent.innerHTML = '';

  const sections = [
    { key: 'career_trajectory_analysis', title: '📈 Career Trajectory', type: 'text' },
    { key: 'skill_prioritization', title: '🎯 Skill Priority', type: 'list' },
    { key: 'industry_trends', title: '📊 Industry Trends', type: 'list' },
    { key: 'learning_strategy', title: '📚 Learning Strategy', type: 'text' },
    { key: 'market_opportunities', title: '💼 Market Opportunities', type: 'list' },
    { key: 'networking_advice', title: '🤝 Networking Tips', type: 'list' }
  ];

  sections.forEach(section => {
    if (insights[section.key]) {
      const sectionDiv = document.createElement('div');
      sectionDiv.className = 'insights-section';
      
      const title = document.createElement('h5');
      title.textContent = section.title;
      title.className = 'insights-section-title';
      sectionDiv.appendChild(title);

      if (section.type === 'text') {
        const text = document.createElement('p');
        text.textContent = insights[section.key];
        text.className = 'insights-text-content';
        sectionDiv.appendChild(text);
      } else if (section.type === 'list' && Array.isArray(insights[section.key])) {
        const list = document.createElement('ul');
        list.className = 'insights-list-content';
        insights[section.key].forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          list.appendChild(li);
        });
        sectionDiv.appendChild(list);
      }

      insightsContent.appendChild(sectionDiv);
    }
  });
}

// =======================================
// 📚 Display Course Recommendations
// =======================================

function displayCourseRecommendations(learningData) {
  // Add course recommendations section after improvement suggestions
  const improvementSection = document.querySelector('.improvement-section');
  let courseSection = document.getElementById('course-recommendations');
  
  if (!courseSection) {
    courseSection = document.createElement('div');
    courseSection.id = 'course-recommendations';
    courseSection.className = 'course-section';
    courseSection.innerHTML = `
      <h4>📚 Recommended Courses</h4>
      <div id="course-list"></div>
      <h4>🎯 Learning Paths</h4>
      <div id="learning-paths"></div>
    `;
    improvementSection.parentNode.insertBefore(courseSection, improvementSection.nextSibling);
  }

  // Display courses
  const courseList = document.getElementById('course-list');
  courseList.innerHTML = '';
  
  Object.entries(learningData.course_recommendations || {}).forEach(([skill, courses]) => {
    const skillDiv = document.createElement('div');
    skillDiv.className = 'skill-courses';
    skillDiv.innerHTML = `<h5>${skill}</h5>`;
    
    courses.slice(0, 2).forEach(course => {
      const courseCard = document.createElement('div');
      courseCard.className = 'course-card';
      courseCard.innerHTML = `
        <div class="course-info">
          <strong>${course.title}</strong>
          <span class="course-provider">${course.provider}</span>
          <span class="course-details">${course.duration} • ${course.level} • ⭐ ${course.rating}</span>
          <span class="course-price">${course.price}</span>
        </div>
      `;
      skillDiv.appendChild(courseCard);
    });
    
    courseList.appendChild(skillDiv);
  });

  // Display learning paths
  const pathsList = document.getElementById('learning-paths');
  pathsList.innerHTML = '';
  
  (learningData.suggested_learning_paths || []).forEach(path => {
    const pathCard = document.createElement('div');
    pathCard.className = 'learning-path-card';
    pathCard.innerHTML = `
      <div class="path-header">
        <h5>${path.name}</h5>
        <span class="completion-badge">${path.completion_percentage}% Complete</span>
      </div>
      <p>${path.description}</p>
      <div class="path-details">
        <span>Duration: ${path.duration}</span>
        <span>Skills needed: ${path.skills_needed}</span>
      </div>
    `;
    pathsList.appendChild(pathCard);
  });
}

// =======================================
// 📊 Analytics Dashboard
// =======================================

function loadAnalyticsDashboard() {
  fetch('http://127.0.0.1:5000/get-analytics')
    .then(res => res.json())
    .then(data => {
      updateAnalyticsDashboard(data);
    })
    .catch(error => {
      console.error('Error loading analytics:', error);
      // Load from localStorage as fallback
      loadLocalAnalytics();
    });
}

function updateAnalyticsDashboard(analyticsData) {
  const resultsContainer = document.getElementById('results');
  
  resultsContainer.innerHTML = `
    <div class="container">
      <h2>📊 Analytics Dashboard</h2>
      
      <div class="analytics-grid">
        <!-- Performance Overview -->
        <div class="card analytics-card">
          <div class="card__body">
            <h3>Performance Overview</h3>
            <div class="metrics-grid">
              <div class="metric">
                <span class="metric-value">${analyticsData.user_progress.total_analyses}</span>
                <span class="metric-label">Total Analyses</span>
              </div>
              <div class="metric">
                <span class="metric-value">${analyticsData.performance_metrics.average_resume_score}</span>
                <span class="metric-label">Avg Resume Score</span>
              </div>
              <div class="metric">
                <span class="metric-value">${analyticsData.performance_metrics.average_interview_score}</span>
                <span class="metric-label">Avg Interview Score</span>
              </div>
              <div class="metric">
                <span class="metric-value">+${analyticsData.performance_metrics.improvement_rate}%</span>
                <span class="metric-label">Improvement Rate</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Skill Demand Chart -->
        <div class="card analytics-card">
          <div class="card__body">
            <h3>Market Demand Trends</h3>
            <canvas id="skillDemandChart" width="400" height="200"></canvas>
          </div>
        </div>

        <!-- Progress Timeline -->
        <div class="card analytics-card full-width">
          <div class="card__body">
            <h3>Recent Activity</h3>
            <div class="activity-timeline" id="activity-timeline"></div>
          </div>
        </div>

        <!-- Skill Growth -->
        <div class="card analytics-card">
          <div class="card__body">
            <h3>Top Growing Skills</h3>
            <div class="skill-growth-list" id="skill-growth"></div>
          </div>
        </div>

        <!-- Learning Progress -->
        <div class="card analytics-card">
          <div class="card__body">
            <h3>Learning Progress</h3>
            <canvas id="progressChart" width="400" height="200"></canvas>
          </div>
        </div>
      </div>
    </div>
  `;

  // Create charts
  createSkillDemandChart(analyticsData.skill_trends.market_demand);
  createProgressChart(analyticsData.user_progress);
  updateActivityTimeline(analyticsData.recent_activity);
  updateSkillGrowth(analyticsData.skill_trends.fastest_growing);
}

function createSkillDemandChart(demandData) {
  const ctx = document.getElementById('skillDemandChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(demandData),
      datasets: [{
        label: 'Market Demand %',
        data: Object.values(demandData),
        backgroundColor: 'rgba(33, 128, 141, 0.8)',
        borderColor: 'rgba(33, 128, 141, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}

function createProgressChart(progressData) {
  const ctx = document.getElementById('progressChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Resume Analyses', 'Interview Analyses'],
      datasets: [{
        data: [progressData.resume_analyses, progressData.interview_analyses],
        backgroundColor: [
          'rgba(33, 128, 141, 0.8)',
          'rgba(168, 75, 47, 0.8)'
        ],
        borderColor: [
          'rgba(33, 128, 141, 1)',
          'rgba(168, 75, 47, 1)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

function updateActivityTimeline(activities) {
  const timeline = document.getElementById('activity-timeline');
  timeline.innerHTML = '';
  
  activities.forEach(activity => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = `
      <div class="timeline-date">${activity.date}</div>
      <div class="timeline-content">
        <div class="timeline-type ${activity.type}">${activity.type}</div>
        <div class="timeline-score">Score: ${activity.score}%</div>
        ${activity.improvement ? `<div class="timeline-improvement">+${activity.improvement}% improvement</div>` : ''}
        ${activity.skills_gap ? `<div class="timeline-gap">${activity.skills_gap} skills gap</div>` : ''}
      </div>
    `;
    timeline.appendChild(item);
  });
}

function updateSkillGrowth(growingSkills) {
  const skillList = document.getElementById('skill-growth');
  skillList.innerHTML = '';
  
  growingSkills.forEach((skill, index) => {
    const item = document.createElement('div');
    item.className = 'growth-item';
    item.innerHTML = `
      <span class="growth-rank">${index + 1}</span>
      <span class="growth-skill">${skill}</span>
      <span class="growth-trend">📈</span>
    `;
    skillList.appendChild(item);
  });
}

// =======================================
// 💾 Local Storage Functions
// =======================================

function saveAnalysisToLocalStorage(type, data) {
  const analyses = JSON.parse(localStorage.getItem('skillsync_analyses') || '[]');
  const analysis = {
    id: Date.now(),
    type: type,
    timestamp: new Date().toISOString(),
    data: data
  };
  
  analyses.unshift(analysis);
  if (analyses.length > 50) analyses.splice(50); // Keep only last 50
  
  localStorage.setItem('skillsync_analyses', JSON.stringify(analyses));
}

function loadLocalAnalytics() {
  const analyses = JSON.parse(localStorage.getItem('skillsync_analyses') || '[]');
  
  // Generate analytics from local data
  const resumeAnalyses = analyses.filter(a => a.type === 'resume');
  const interviewAnalyses = analyses.filter(a => a.type === 'interview');
  
  const mockAnalytics = {
    user_progress: {
      total_analyses: analyses.length,
      resume_analyses: resumeAnalyses.length,
      interview_analyses: interviewAnalyses.length,
      average_improvement: 18,
      skills_learned: 5
    },
    skill_trends: {
      market_demand: {
        "Python": 95,
        "JavaScript": 92,
        "React": 88,
        "AWS": 85,
        "Docker": 82
      },
      fastest_growing: ["Machine Learning", "Docker", "Kubernetes", "React", "TypeScript"]
    },
    performance_metrics: {
      average_resume_score: 74,
      average_interview_score: 78,
      improvement_rate: 18,
      completion_rate: 87
    },
    recent_activity: analyses.slice(0, 5).map(a => ({
      date: new Date(a.timestamp).toISOString().split('T')[0],
      type: a.type,
      score: a.data.similarity_score || a.data.overall_score || 75,
      improvement: Math.floor(Math.random() * 15) + 5
    }))
  };
  
  updateAnalyticsDashboard(mockAnalytics);
}

// =======================================
// 📄 Download Report Functions
// =======================================

let currentInterviewData = null; // Store current interview data for download

function downloadInterviewReport() {
  if (!currentInterviewData) {
    alert('No interview data available to download.');
    return;
  }

  const data = currentInterviewData;
  const reportContent = `
SKILLSYNC INTERVIEW ANALYSIS REPORT
Generated on: ${new Date().toLocaleDateString()}

OVERALL INTERVIEW SCORE: ${data.overall_score || 'N/A'}%

SPEECH ANALYSIS:
• Confidence Score: ${data.speech_analysis?.confidence_score || 'N/A'}%
• Clarity Score: ${data.speech_analysis?.clarity_score || 'N/A'}%
• Hesitation Rate: ${data.speech_analysis?.hesitation_rate || 'N/A'}%
• Total Words: ${data.speech_analysis?.total_words || 'N/A'}
• Average Sentence Length: ${data.speech_analysis?.avg_sentence_length || 'N/A'} words

EMOTIONAL ANALYSIS:
• Overall Sentiment: ${data.sentiment_analysis?.overall_sentiment || 'N/A'}
• Dominant Emotion: ${data.sentiment_analysis?.dominant_emotion || 'N/A'}
• Polarity Score: ${data.sentiment_analysis?.polarity || 'N/A'}

CONTENT QUALITY:
• Content Score: ${data.content_analysis?.content_quality_score || 'N/A'}%
• Technical Skills Mentioned: ${data.content_analysis?.technical_skills_mentioned?.join(', ') || 'None'}
• Soft Skills Mentioned: ${data.content_analysis?.soft_skills_mentioned?.join(', ') || 'None'}

STRENGTHS:
${data.performance_summary?.strengths?.map(strength => `• ${strength}`).join('\n') || 'None listed'}

AREAS FOR IMPROVEMENT:
${data.performance_summary?.areas_for_improvement?.map(area => `• ${area}`).join('\n') || 'None listed'}

RECOMMENDATIONS:
${data.feedback?.map((rec, index) => `${index + 1}. ${rec}`).join('\n') || 'None provided'}

${data.transcript ? `\nTRANSCRIPT:\n"${data.transcript}"` : ''}

This report was generated by SkillSync - Professional Resume & Interview Analysis Tool.
  `;
  
  const blob = new Blob([reportContent], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `SkillSync_Interview_Report_${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function downloadResumeReport() {
  // Simple text-based report generation
  const score = document.getElementById('similarity-score').textContent;
  const matchedSkills = Array.from(document.querySelectorAll('#matched-skills .skill-tag')).map(el => el.textContent);
  const missingSkills = Array.from(document.querySelectorAll('#missing-skills .skill-tag')).map(el => el.textContent);
  const suggestions = Array.from(document.querySelectorAll('#improvement-suggestions li')).map(el => el.textContent);
  
  const reportContent = `
SKILLSYNC RESUME ANALYSIS REPORT
Generated on: ${new Date().toLocaleDateString()}

OVERALL MATCH SCORE: ${score}%

MATCHED SKILLS:
${matchedSkills.map(skill => `• ${skill}`).join('\n')}

MISSING SKILLS:
${missingSkills.map(skill => `• ${skill}`).join('\n')}

IMPROVEMENT SUGGESTIONS:
${suggestions.map((suggestion, index) => `${index + 1}. ${suggestion}`).join('\n')}

This report was generated by SkillSync - Professional Resume & Interview Analysis Tool.
  `;
  
  const blob = new Blob([reportContent], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `SkillSync_Resume_Report_${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ======================
// 💡 Utility Functions
// ======================

function showLoadingModal() {
  document.getElementById('loading-modal').classList.remove('hidden');
}

function hideLoadingModal() {
  document.getElementById('loading-modal').classList.add('hidden');
}

function startProgressBar(progressId, textId) {
  const progressBar = document.getElementById(progressId);
  const progressText = document.getElementById(textId);
  let width = 0;
  const interval = setInterval(() => {
    if (width >= 100) {
      clearInterval(interval);
    } else {
      width += 1;
      progressBar.style.width = `${width}%`;
      progressText.textContent = `${width}% complete`;
    }
  }, 15);
}

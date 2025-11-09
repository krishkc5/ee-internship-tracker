// Application state
let allJobs = [];
let filteredJobs = [];
let applicationStatus = {};

// Load application status from localStorage
function loadApplicationStatus() {
    const stored = localStorage.getItem('jobApplicationStatus');
    if (stored) {
        applicationStatus = JSON.parse(stored);
    }
}

// Save application status to localStorage
function saveApplicationStatus() {
    localStorage.setItem('jobApplicationStatus', JSON.stringify(applicationStatus));
}

// Update job status
function updateJobStatus(jobId, status) {
    applicationStatus[jobId] = {
        status: status,
        updatedAt: new Date().toISOString()
    };
    saveApplicationStatus();
    renderJobs();
    updateStats();
}

// Fetch jobs from data file
async function fetchJobs() {
    try {
        // Try to fetch from the aggregated jobs file
        // This path will be relative to the GitHub Pages site
        const response = await fetch('../data/jobs_all.json');

        if (!response.ok) {
            throw new Error('Failed to fetch jobs');
        }

        allJobs = await response.json();
        filteredJobs = allJobs;

        renderJobs();
        updateStats();
        updateLastUpdated();
    } catch (error) {
        console.error('Error fetching jobs:', error);
        document.getElementById('jobsList').innerHTML = `
            <div class="no-jobs">
                <h3>No jobs available yet</h3>
                <p>The scraper hasn't run yet or there was an error loading jobs.</p>
                <p>Please check back later or run the scraper manually.</p>
            </div>
        `;
    }
}

// Render jobs to the page
function renderJobs() {
    const jobsList = document.getElementById('jobsList');

    if (filteredJobs.length === 0) {
        jobsList.innerHTML = '<div class="no-jobs">No jobs match your current filters.</div>';
        return;
    }

    jobsList.innerHTML = filteredJobs.map(job => {
        const status = applicationStatus[job.id]?.status || 'not-applied';
        const statusClass = status.replace('_', '-');

        return `
            <div class="job-card ${status !== 'not-applied' ? status : ''}" data-job-id="${job.id}">
                <div class="job-header">
                    <div>
                        <h3 class="job-title">${escapeHtml(job.title)}</h3>
                        <div class="job-company">${escapeHtml(job.company)}</div>
                    </div>
                    <span class="status-badge status-${statusClass}">
                        ${status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                </div>

                <div class="job-meta">
                    <span>📍 ${escapeHtml(job.location)}</span>
                    <span>📅 ${formatDate(job.posted_date || job.scraped_date)}</span>
                    <span class="source-badge">${escapeHtml(job.source)}</span>
                </div>

                ${job.description ? `
                    <div class="job-description">
                        ${escapeHtml(job.description).substring(0, 200)}${job.description.length > 200 ? '...' : ''}
                    </div>
                ` : ''}

                <div class="job-actions">
                    <a href="${escapeHtml(job.url)}" target="_blank" class="btn btn-primary">
                        View Job
                    </a>
                    ${status === 'not-applied' ? `
                        <button onclick="updateJobStatus('${job.id}', 'applied')" class="btn btn-success">
                            Mark Applied
                        </button>
                    ` : ''}
                    ${status === 'applied' ? `
                        <button onclick="updateJobStatus('${job.id}', 'interviewing')" class="btn btn-warning">
                            Mark Interviewing
                        </button>
                        <button onclick="updateJobStatus('${job.id}', 'not-applied')" class="btn btn-secondary">
                            Reset
                        </button>
                    ` : ''}
                    ${status === 'interviewing' ? `
                        <button onclick="updateJobStatus('${job.id}', 'applied')" class="btn btn-secondary">
                            Back to Applied
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Filter jobs based on search and filters
function filterJobs() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const showNotApplied = document.getElementById('filterNotApplied').checked;
    const showApplied = document.getElementById('filterApplied').checked;
    const showInterviewing = document.getElementById('filterInterviewing').checked;
    const sourceFilter = document.getElementById('sourceFilter').value;

    filteredJobs = allJobs.filter(job => {
        // Search filter
        const matchesSearch = !searchTerm ||
            job.title.toLowerCase().includes(searchTerm) ||
            job.company.toLowerCase().includes(searchTerm) ||
            job.location.toLowerCase().includes(searchTerm) ||
            (job.description && job.description.toLowerCase().includes(searchTerm));

        // Status filter
        const status = applicationStatus[job.id]?.status || 'not-applied';
        const matchesStatus =
            (status === 'not-applied' && showNotApplied) ||
            (status === 'applied' && showApplied) ||
            (status === 'interviewing' && showInterviewing);

        // Source filter
        const matchesSource = sourceFilter === 'all' || job.source === sourceFilter;

        return matchesSearch && matchesStatus && matchesSource;
    });

    renderJobs();
    updateStats();
}

// Update statistics
function updateStats() {
    const totalJobs = allJobs.length;
    const appliedCount = Object.values(applicationStatus).filter(s => s.status === 'applied' || s.status === 'interviewing').length;

    // Calculate new jobs (scraped in the last 24 hours)
    const oneDayAgo = new Date();
    oneDayAgo.setDate(oneDayAgo.getDate() - 1);
    const newJobsCount = allJobs.filter(job => new Date(job.scraped_date) > oneDayAgo).length;

    document.getElementById('totalJobs').textContent = `Total: ${totalJobs}`;
    document.getElementById('appliedCount').textContent = `Applied: ${appliedCount}`;
    document.getElementById('newJobs').textContent = `New: ${newJobsCount}`;
}

// Update last updated timestamp
function updateLastUpdated() {
    if (allJobs.length > 0) {
        const latestJob = allJobs[0]; // Jobs are sorted by scraped_date
        const lastUpdated = new Date(latestJob.scraped_date);
        document.getElementById('lastUpdated').textContent = lastUpdated.toLocaleString();
    }
}

// Export application data
function exportData() {
    const exportData = allJobs.map(job => ({
        title: job.title,
        company: job.company,
        location: job.location,
        url: job.url,
        source: job.source,
        status: applicationStatus[job.id]?.status || 'not-applied',
        updatedAt: applicationStatus[job.id]?.updatedAt || '',
        postedDate: job.posted_date,
        scrapedDate: job.scraped_date
    }));

    const csv = convertToCSV(exportData);
    downloadCSV(csv, 'job_applications.csv');
}

// Convert data to CSV
function convertToCSV(data) {
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];

    for (const row of data) {
        const values = headers.map(header => {
            const value = row[header]?.toString() || '';
            return `"${value.replace(/"/g, '""')}"`;
        });
        csvRows.push(values.join(','));
    }

    return csvRows.join('\n');
}

// Download CSV file
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
}

// Event listeners
document.getElementById('searchInput').addEventListener('input', filterJobs);
document.getElementById('filterNotApplied').addEventListener('change', filterJobs);
document.getElementById('filterApplied').addEventListener('change', filterJobs);
document.getElementById('filterInterviewing').addEventListener('change', filterJobs);
document.getElementById('sourceFilter').addEventListener('change', filterJobs);
document.getElementById('exportBtn').addEventListener('click', exportData);

// Make updateJobStatus available globally
window.updateJobStatus = updateJobStatus;

// Initialize
loadApplicationStatus();
fetchJobs();

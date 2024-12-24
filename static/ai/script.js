// Timer functionality
function updateTimer() {
    const timerElement = document.querySelector('.timer');
    let seconds = 0;
    
    setInterval(() => {
        seconds++;
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        timerElement.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }, 1000);
}

// Tab switching
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });
}

// Pagination
function initializePagination() {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.addEventListener('click', () => {
            pages.forEach(p => p.classList.remove('active'));
            page.classList.add('active');
        });
    });
}

function initializeSubmitButton() {
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.addEventListener('click', () => {
        const programCode = document.querySelector('#programInput').value;
        const testInput = document.querySelector('#testInput').value;
        console.log('Submitting program:', programCode);
        console.log('Test cases:', testInput);
        // Add your submission logic here
    });
}

function loadQuestion(questionNumber) {
    // Select the problem content container
    const question = document.getElementById('problem-content');
    question.innerHTML = 'Loading...';

    // Define the API view URL dynamically based on the question number
    const contestId = document.getElementById('contest').dataset.contestId;
    const apiview = questionNumber === -1 
        ? `${contestId}/question/` 
        : `${contestId}/question/?question_id=${questionNumber}`;

    // Fetch data from the API
    fetch(apiview)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            // Update the question content
            question.innerHTML = `
                <h1>${data.current_question.title}'</h1>
                <p>${data.current_question['description']}</p>
            `;

            // Handle pagination and solved statuses
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = ''; // Clear existing pagination

            data.solved_status.forEach((questionStatus, index) => {
                const page = document.createElement('div');
                page.classList.add('page');
                if (questionStatus) {
                    page.classList.add('solved');
                }
                page.textContent = index + 1;
                page.addEventListener('click', () => loadQuestion(index+1));
                pagination.appendChild(page);
            });
        })
        .catch(error => {
            // Handle any errors
            console.error(error);
            question.innerHTML = 'An error occurred while loading the question.';
        });
}


// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    updateTimer();
    initializeTabs();
    initializePagination();
    initializeSubmitButton();
    loadQuestion(-1);
});
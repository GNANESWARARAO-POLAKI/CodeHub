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

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    updateTimer();
    initializeTabs();
    initializePagination();
    initializeSubmitButton();
});
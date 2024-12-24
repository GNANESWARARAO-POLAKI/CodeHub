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

function loadQuestion(questionNumber){
    const question = document.querySelector('.problem-content');
    question.innerHTML='';
    if (questionNumber == -1){
        apiview={{contest.id}}+'/question/';
    }
    else{
        apiview={{contest.id}}+'/question/'+questionNumber;
    }
    fetch(apiview).then(response => response.json()).then(data => {
        question.innerHTML = '<h1>'+data.current_question.title+'</h1><p>'+data.current_question.description+'</p>';

        console.log(data);
        pagination=document.getElementById('pagination');
        pagination.innerHTML='';
        data.solved_status.forEach((question_status, index) => {
            const questionNumber = index + 1; // Get the current question number
            const questionName = question_status.id; // Access the question name or property
            console.log(`${questionNumber} ${questionName}`);
        });
        


    });
   
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    updateTimer();
    initializeTabs();
    initializePagination();
    initializeSubmitButton();
});
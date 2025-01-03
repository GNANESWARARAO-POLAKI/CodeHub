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


function initializeSubmitButton() {
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.addEventListener('click', () => {
        const programCode = document.querySelector('#programInput').value;
        const question_number = document.querySelector('#questionNumber').value;
        const language=document.getElementById('language').value;
        console.log('Submitting program:', programCode);
        fetch(`/codelife/submit/${question_number}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Or application/json, if your backend expects JSON
            },
            body: `code=${encodeURIComponent(programCode)}&language=${language}`, // Ensure keys match backend
        }).then(response => response.json()).then(data => {
            console.log('Submission result:', data);
            
        }); 
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
            // console.log(data);
            // Update the question content
            question.innerHTML = `
                <h1>${data.current_question.title}'</h1>
                <p>${data.current_question['description']}</p>
            `;
            const lives=document.getElementById('lives');
            lives.innerHTML='';
            for (let i=0;i<data.current_question.lives-data.current_question.lost_submissions;i++){
                lives.innerHTML+=`<span class="heart">❤️</span>`;
            }
            for(let i=0;i<data.current_question.lost_submissions;i++){
                lives.innerHTML+=`<span class="heart">🩶</button>`;
            }
             const pagination = document.getElementById('pagination');
            pagination.innerHTML='';
            current_index=0;
            final_index=0;
            data.solved_status.forEach((questionStatus, index) => {
                // console.log(questionStatus);
                // console.log(index);
                final_index=index;
                if (questionStatus.solved || data.current_question.id === questionStatus.question_id) {
                    
                    pagination.innerHTML+=`<button  class="page active" onclick=loadQuestion(${questionStatus.question_id})>${index+1}</button>
                    <input type="hidden" id="questionNumber" value="${index+1}">`;
                    current_index=index;
                }
                else {
                    pagination.innerHTML+=`<button class="page" onclick=loadQuestion(${questionStatus.question_id})>${index+1}</button>`;
                }
            });
            if(current_index!=0){
                pagination.innerHTML = `<button class="prev" onclick=loadQuestion(${data.current_question.id-1   })>◀</button>`+pagination.innerHTML; 
            }
            if(final_index!=current_index){
            pagination.innerHTML+=`<button class="prev" onclick=loadQuestion(${data.current_question.id+1})>▶</button>`;
            }
            // const testInput = document.getElementById('testInput');
            // testInput.value = data.current_question.sample_testcase.input;

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
    initializeSubmitButton();
    loadQuestion(-1);
});




// require.config({
//     paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.37.1/min/vs' }  
// });

// require(['vs/editor/editor.main'], function () {
//     var editor = monaco.editor.create(document.getElementById('input-field'), {
//         value: [
//             'def hello_world():',
//             '    print("Hello, world!")',
//             '',
//             'hello_world()'
//         ].join('\n'),
//         language: 'python',  // Set default language to Python
//         theme: 'vs-dark',    // Set the theme to Dark Mode
//         scrollbar: {
//             vertical: 'auto',  // Enable vertical scrollbar
//             horizontal: 'auto' // Enable horizontal scrollbar
//         },
//         minimap: {
//             enabled: false  // Disable the minimap to reduce clutter
//         },
//         lineNumbers: 'on',  // Show line numbers
//         wordWrap: 'on',  // Enable word wrapping
//         autoClosingBrackets: true,  // Automatically close brackets
//         autoIndent: true,  // Auto indent code
//         suggest: {
//             filterGraceful: true  // Enable graceful filtering for suggestions
//         },
//         scrollBeyondLastLine: false  // Disable scrolling beyond the last line
//     });
// });




// editor text area 



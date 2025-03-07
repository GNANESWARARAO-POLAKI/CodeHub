

// disable right click and inspect element
// remove tab switch 

// document.addEventListener("contextmenu", event => event.preventDefault());
// document.addEventListener("keydown", event => {
//     if (event.key === "F12" || (event.ctrlKey && event.shiftKey && event.key === "I")) {
//         event.preventDefault();
//     }
// });

// document.addEventListener("visibilitychange", function() {
//     if (document.hidden) {
//         alert("Switching tabs is not allowed during the contest!");
//         const contestId=document.getElementById('contest').dataset.contestId;
//         window.location.href = `${contestId}/contest_results`;  
//     }
// });




function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const  tab_contents=document.querySelectorAll('.tab_content');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab_contents.forEach(t=>t.style.display='none' );
            target_tab=tab.dataset.target;
            if (target_tab==='leaderboard-content'){
                get_leaderboard();
            }
            tab.classList.add('active');
            document.getElementById(target_tab).style.display='block';
        });
    });
}

function get_leaderboard(){
    const leaderboard =document.getElementById('leaderboard-content');
    const contestId=document.getElementById('contest').dataset.contestId;
    fetch(`${contestId}/leaderboard`).then(response=>{
        if (!response.ok){
            throw new Error(' error occureed when fetching the leaderboard')
        }
        return response.json();
    }
    ).then(data=>{

        leaderboard.innerHTML=`<h1>Leaderboard</h1><div id='leaderboard-table-container'><table id="leaderboard-table"><thead><tr><td>Rank</td><td>Jntu No</td><td>Username</td><td>Score</td><td>Last Submission</td><td>Year</td></tr></thead><tbody></tbody></table></div>`;
        let rowsHTML = '';
        data.participants.forEach((item) => {
            rowsHTML += `
                <tr>
                    <td>${item.rank}</td>
                    <td>${item.jntuno}</td>
                    <td><a style='text-decoration:none;color:var(--text-secondary);' href="../user/${item.username}">${item.username}</a></td>
                    <td>${item.score}</td>
                    <td>${(new Date(item.last_activity)).toLocaleTimeString()}</td>
                    <td>${item.year}</td>
                </tr>
            `;
        });
        const tableBody = document.querySelector('#leaderboard-table tbody'); // Get the table body
        tableBody.innerHTML = rowsHTML;
        console.log(data);
    }
    )
}
// Pagination

function loadQuestion(questionNumber) {
    // Select the problem content container
    const question = document.getElementById('problem-content');
    document.getElementById('mainframe-cover').style.display='flex';
    question.innerHTML = 'Loading...';
    
    
    if (questionNumber!=-1){
        const c_code=document.getElementById('c-code').value;
        const pyhton_code=document.getElementById('python-code').value;
        const cpp_code=document.getElementById('cpp-code').value;
        const java_code=document.getElementById('java-code').value;
        const question_number = document.getElementById('question_id').dataset.questionId;
        const data={
            'question_id':question_number,
            'c':c_code,
            'cpp':cpp_code,
            'python':pyhton_code,
            'java':java_code
       }
    fetch('save_temporary_code/',{
        method:'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', 
        },
        body: JSON.stringify(data),
    }).catch(error=>{
        console.error(error);
    })}
    const contestId = document.getElementById('contest').dataset.contestId;
    const apiview = questionNumber === -1 
        ? `${contestId}/question/` 
        : `${contestId}/question/?question_id=${questionNumber}`;
    
    fetch(apiview)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error); // Extract error message from JSON
                });
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            question.innerHTML = `
              <div id="problem-content" class="tab_content">
                    <div class="question-flex">
                        <h1 id="title">${data.current_question.title}</h1>
                  <h2>Score :<i id="question-score">${data.current_question.score}</i></h2>
                  </div>
                <hr><br>
                ${data.current_question['description']}
            `;
            if(data.current_question.status){
                document.getElementById('solved-status').innerHTML='solved';
            }
            else{
                document.getElementById('solved-status').innerHTML='unsolved';
            }
            
            document.getElementById('total-score').innerHTML=`${data.total_score}`;
            document.getElementById('current-score').innerHTML=`${data.current_score}`;
            const lives=document.getElementById('lives');
            lives.innerHTML='';
            const submit=document.getElementById('submit-btn');
            if (data.current_question.lost_submissions>=data.current_question.lives){
                data.current_question.lost_submissions=data.current_question.lives;
                submit.disabled=true;
                submit.setAttribute('data-tooltip','you have lost all lifes of this question')
            }
            else{
                submit.disabled=false;
                submit.setAttribute('data-tooltip','Click to Submit');
            }
            for (let i=0;i<data.current_question.lives-data.current_question.lost_submissions;i++){
                lives.innerHTML+=`<span class="heart" heart-type='red'>❤️</span>`;
            }
            for(let i=0;i<data.current_question.lost_submissions;i++){
                lives.innerHTML+=`<span class="heart" heart-type='white'>🩶</span>`;
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
                    
                    // pagination.innerHTML+=`<button  class="page active" onclick=loadQuestion(${questionStatus.question_id})>${index+1}</button>`;
                    if (data.current_question.id === questionStatus.question_id){
                        current_index=index;
                        pagination.innerHTML+=`<button id='question_id' class="page current" data-question-id="${questionStatus.question_id}" onclick=loadQuestion(${questionStatus.question_id}) >${index+1}</button>`;
                    }
                    else{
                        pagination.innerHTML+=`<button   class="page active" onclick=loadQuestion(${questionStatus.question_id}) data-tooltip='solved'>${index+1}</button>`;
                    }
                }
                else {
                    pagination.innerHTML+=`<button class="page" onclick=loadQuestion(${questionStatus.question_id}) data-tooltip='unsolved'>${index+1}</button>`;
                }
            });
            if(current_index!=0){
                pagination.innerHTML = `<button class="prev" onclick=loadQuestion(${data.current_question.id-1   }) data-tooltip='previous'>◀</button>`+pagination.innerHTML; 
            }
            if(final_index!=current_index){
            pagination.innerHTML+=`<button class="prev" onclick='loadQuestion(${data.current_question.id+1})' data-tooltip='next'>▶</button>`;
            }
            else{
                pagination.innerHTML+=` <button class='page active'style='float:right;right:10px;position:absolute;' onclick='endContest()'>End contest</button>`
            }
            // const testInput = document.getElementById('testInput');
            // testInput.value = data.current_question.sample_testcase.input;
            if (data.testcase_data){
            testcase_handling(data.testcase_data);
            }
            else{
                final_result=document.getElementById('final-result');
                final_result.innerHTML=``;
                final_result_header=document.getElementById('final-result-header');
                final_result_header.innerHTML=``;
            }

            if (data.scripts){
                document.getElementById('c-code').innerHTML=data.scripts.c;
                document.getElementById('python-code').innerHTML = data.scripts.python;
                document.getElementById('cpp-code').innerHTML = data.scripts.cpp;
                document.getElementById('java-code').innerHTML = data.scripts.java;
                const textarea1 = document.getElementById("textarea1");
                language=document.getElementById('language').value;
                textarea1.value=data.scripts[language];
                updateCode();
            }
            document.getElementById('mainframe-cover').style.display='none';
           
        })
        .catch(error => {
            // Handle any errors
            console.error('Error object:', error);
            console.error('Error:', error.message || 'An unknown error occurred.');
            question.innerHTML = 'An error occurred while loading the question.';
            document.getElementById('mainframe-cover').innerHTML=`<h2 style='color:red'>
            ${error.message}</h2>. Wait until it is resolved or try refresh.`;
            // document.getElementById('mainframe-cover').innerHTML=`
            // <img id=heart' src='media/core_media/sad.gif' alt='no img' width='200px' height='200px'>
            // `;
         // Duration of one GIF cycle in milliseconds (Adjust this!)

        
           
            // document.getElementById('mainframe-cover').style.display='none';
        });
        
}


function ContestEnded(){
   const maincover=document.createElement('div');
   maincover.classList.add('maincontent-cover');
   maincover.style.display='flex';
    maincover.innerHTML=`<h1>Contest Ended</h1><br><h2>Try to refesh to see reasults.</h2>`;
    document.body.appendChild(maincover);
    document.getElementById('submit-btn').disabled=true;
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // updateTimer();
    initializeTabs();
    loadQuestion(-1);
    initializeSubmitButton();
    initializeRunButton();
    const cover = document.getElementById('cover-content');
    const fs = document.getElementById('enable-fullscreen');

    function requestFullScreen() {
        let elem = document.documentElement;

        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { // Firefox
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { // Chrome, Safari, Opera
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { // IE/Edge
            elem.msRequestFullscreen();
        }
    }

    function isFullScreen() {
        return document.fullscreenElement || 
               document.mozFullScreenElement || 
               document.webkitFullscreenElement || 
               document.msFullscreenElement || 
               (window.innerHeight === screen.height);
    }

    function toggleFullScreenButton() {
        if (isFullScreen()) {
            cover.style.display = "none";
            fs.style.display = "none";
            // console.log('Full screen enabled');
        } else {
            // cover.style.display = "flex";
            // fs.style.display = "flex"; 
            // console.log('Full screen disabled');
        }
    }

    document.getElementById('fullscreen').addEventListener("click", function () {
        requestFullScreen();
    });

    // Detect full-screen exit/change
    document.addEventListener("fullscreenchange", toggleFullScreenButton);
    document.addEventListener("mozfullscreenchange", toggleFullScreenButton);
    document.addEventListener("webkitfullscreenchange", toggleFullScreenButton);
    document.addEventListener("msfullscreenchange", toggleFullScreenButton);

    // Detect F11 press
    document.addEventListener("keydown", function (event) {
        if (event.key === "F11") {
            setTimeout(toggleFullScreenButton, 500); // Delay to allow full-screen detection
        }
    });

    // Detect window resize (useful for F11 full-screen)
    window.addEventListener("resize", () => {
        setTimeout(toggleFullScreenButton, 500);
    });

    // Initial check
    toggleFullScreenButton();
});




function endContest(){
    const cover = document.getElementById('cover-content');
    cover.style.display = 'flex';
    document.getElementById('end-contest').style.display='flex';
}
// function confirmEndContest(){



    
// }
function cancelContent(button){
    let parent=button.parentElement;
    let grandParentDiv = parent.parentElement;
    grandParentDiv.style.display='none';
    const cover = document.getElementById('cover-content');
    cover.style.display = 'none';

}  
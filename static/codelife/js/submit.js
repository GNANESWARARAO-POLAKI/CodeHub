function initializeSubmitButton() {
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.addEventListener('click', () => {
        submitBtn.disabled=true;
        const lives=document.querySelectorAll('#lives span');
        let reds=0;
        let whites=0;
        lives.forEach( heart=> {
            const type=heart.getAttribute('heart-type');
            if (type==='red'){
                reds+=1;
            }
            else{
                whites+=1;
            }
        });
        if (reds==0){
            const cover = document.getElementById('cover-content');
            cover.style.display = 'flex';
            const nolives=document.getElementById('failed-submission');
            nolives.style.display='flex';
            console.log('it is executing')
            // Allow the browser to render the image before scheduling its removal
            // console.log(performance.now())
            
            submitBtn.disabled = true;
            return;
        }

        const programCode = document.querySelector('#textarea1').value;
        const question_number = document.getElementById('question_id').dataset.questionId;
        const language=document.getElementById('language').value;
//  console.log('Submitting program:', programCode);
        const c_code=document.getElementById('c-code').value;
        const pyhton_code=document.getElementById('python-code').value;
        const cpp_code=document.getElementById('cpp-code').value;
        const java_code=document.getElementById('java-code').value;
        const data={
            'code':programCode,
            'language':language,
            'temp_code_data':{
                    'question_id':question_number,
                    'c':c_code,
                    'cpp':cpp_code,
                    'python':pyhton_code,
                    'java':java_code
            }
        }
        fetch(`/codelife/submit/${question_number}`, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', 
            },
            body: JSON.stringify(data),
        }).then(response => {
            if (response.status === 200) {
                return response.json(); // Process response if successful
            } else if (response.status === 400) {
                alert('The contest has ended.click ok to refresh.');
                window.location.reload();
                // throw new Error("Bad Request: The contest has ended.");
            } else {
                throw new Error(`Unexpected error: ${response.status}`);
            }
        }).then(data => {
            console.log('Submission result:', data);
            const testcase_containers=document.querySelectorAll('.testcase-container');
            testcase_containers.forEach(container => container.remove());
            if (data.success===false){
                const cover = document.getElementById('cover-content');
                cover.style.display = 'flex';
                const image=document.getElementById('failure-img');
                image.style.display='block';
                // Allow the browser to render the image before scheduling its removal
                console.log(performance.now())
                setTimeout(() => {
                   
                    // cover.innerHTML = '';
                    image.style.display='none';
                    cover.style.display = 'none';
                    console.log(performance.now())
                
                }, 2000); 
            }
            // 
            else {
                
                const cover = document.getElementById('cover-content');
                cover.style.display = 'flex';
                const image=document.getElementById('success-img');
                image.style.display='block';
                if(data.score!==0){
                    const currenet_Score=document.getElementById('current-score');
                    currenet_Score.innerHTML=`${data.current_score}`;
                    document.getElementById('solved-status').innerHTML='solved';
                }
                // Allow the browser to render the image before scheduling its removal
                console.log(performance.now())
                setTimeout(() => {
                    // cover.innerHTML = '';
                    image.style.display='none';
                    cover.style.display = 'none';
                    console.log(performance.now())
                }, 2000); 

            }
            testcase_handling(data);
        });
        // console.log(performance.now())
        setTimeout(() => {
            let reds=0;
            let whites=0
            lives.forEach( heart=> {
                const type=heart.getAttribute('heart-type');
                if (type==='red'){
                    reds+=1;
                }
                else{
                    whites+=1;
                }
            });
            if (reds!==0){
            submitBtn.disabled = false;
            submitBtn.setAttribute('data-tooltip','you last all your lives for thiis question');

            }
            // console.log(performance.now())
        }, 10000);
        
    });
   
    
}




function initializeRunButton() {
    const runBtn = document.getElementById('run-btn');
    runBtn.addEventListener('click', () => {
        runBtn.disabled=true;
        const lives=document.querySelectorAll('#lives span');
        let reds=0;
        let whites=0;
        lives.forEach( heart=> {
            const type=heart.getAttribute('heart-type');
            if (type==='red'){
                reds+=1;
            }
            else{
                whites+=1;
            }
        });
        if (reds==0){
            const cover = document.getElementById('cover-content');
            cover.style.display = 'flex';
            const nolives=document.getElementById('failed-submission');
            nolives.style.display='flex';
            console.log('it is executing')
            // Allow the browser to render the image before scheduling its removal
            // console.log(performance.now())
            
            runBtn.disabled = true;
            return;
        }

        const programCode = document.querySelector('#textarea1').value;
        const question_number = document.getElementById('question_id').dataset.questionId;
        const language=document.getElementById('language').value;
//  console.log('Submitting program:', programCode);
        const c_code=document.getElementById('c-code').value;
        const pyhton_code=document.getElementById('python-code').value;
        const cpp_code=document.getElementById('cpp-code').value;
        const java_code=document.getElementById('java-code').value;
        const contest_id=document.getElementById('contest').dataset.contestId;
        const data={
            'contest_id':contest_id,
            'code':programCode,
            'language':language,
            'temp_code_data':{
                    'question_id':question_number,
                    'c':c_code,
                    'cpp':cpp_code,
                    'python':pyhton_code,
                    'java':java_code
            }
        }
        fetch(`/compticode/run_code/${question_number}`, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', 
            },
            body: JSON.stringify(data),
        }).then(response => response.json()).then(data => {
            console.log('Submission result:', data);
            const testcase_containers=document.querySelectorAll('.testcase-container');
            testcase_containers.forEach(container => container.remove());
            // if (data.success===false){
            //     // const cover = document.getElementById('cover-content');
            //     // cover.style.display = 'flex';
            //     // const image=document.getElementById('failure-img');
            //     // image.style.display='block';
            //     // Allow the browser to render the image before scheduling its removal
            //     // console.log(performance.now())
            //     // setTimeout(() => {
                   
            //     //     // cover.innerHTML = '';
            //     //     image.style.display='none';
            //     //     cover.style.display = 'none';
            //     //     console.log(performance.now())
                
            //     // }, 2000); 
            // }
            // // 
            // else {
            //     const cover = document.getElementById('cover-content');
            //     cover.style.display = 'flex';
            //     const image=document.getElementById('success-img');
            //     image.style.display='block';
            //     if(data.score!==0){
            //         const currenet_Score=document.getElementById('current-score');
            //         currenet_Score.innerHTML=`${data.current_score}`;
            //         document.getElementById('solved-status').innerHTML='solved';
            //     }
            //     // Allow the browser to render the image before scheduling its removal
            //     console.log(performance.now())
            //     setTimeout(() => {
            //         // cover.innerHTML = '';
            //         image.style.display='none';
            //         cover.style.display = 'none';
            //         console.log(performance.now())
            //     }, 2000); 

            // }


            // testcase_handling(data);
            run_testcase_handling(data);
        });
        // console.log(performance.now())
        runBtn.setAttribute('data-tooltip','Button is disbled for 10sec ')
        setTimeout(() => {
            let reds=0;
            let whites=0
            lives.forEach( heart=> {
                const type=heart.getAttribute('heart-type');
                if (type==='red'){
                    reds+=1;
                }
                else{
                    whites+=1;
                }
            });
            if (reds!==0){
            runBtn.disabled = false;
            runBtn.setAttribute('data-tooltip','Click run code');

            }
            // console.log(performance.now())
        }, 10000);
        
    });
   
    
}

function run_testcase_handling(data){
    final_result=document.getElementById('final-result');
    final_result_header=document.getElementById('final-result-header');
    final_result.innerHTML=``;
    no=1;
    pass=true;
    // if (data.success==false){
    //     const lives=document.querySelectorAll('#lives span');
    //     let reds=0;
    //     let whites=0;
    //     lives.forEach( heart=> {
    //         const type=heart.getAttribute('heart-type');
    //         if (type==='red'){
    //             reds+=1;
    //         }
    //         else{
    //             whites+=1;
    //         }
    //     });
    //     if (reds!=0){
    //         const heart_to_change=lives[reds-1];
    //     heart_to_change.innerHTML='🩶'
    //     heart_to_change.setAttribute('heart-type','white');
    //     }
        
    // }
    // else{
    //     pass;
    // }
    data.sample_testcase.forEach(testcase => {
        if (testcase.success===true ){
            final_result.innerHTML += `
            <button id="testcase-btn-${no}" class="testcase-button" 
                
                onclick="view_testcase(${no})">
                🔽 ${no} - Correct Answer 
            </button>
        `;            create_testcase_content(no,testcase.input,testcase.expected_output,testcase.actual_output);
        }
        else{
            final_result.innerHTML += `
            <button id="testcase-btn-${no}" class="testcase-button" 
                onclick="view_testcase(${no})">
                🔽 ${no} ${testcase.error} 
            </button>
        `;
        // final_result.innerHTML+=`<button  style='background:var(--bg-tertiary);cursor:pointer;border:1px solid var(--border-color);padding:10px;border-radius:5px'onclick='view_testcase(${no})''>🔓 ${no}-${testcase.error} --score:0 --View Details</button><br>`;
            pass=false;
            if (testcase.error==='wrong_answer'){
                create_testcase_content(no,testcase.input,testcase.expected_output,testcase.actual_output);
            }
            else{
                testcase_container=document.createElement('div');
                testcase_container.classList.add('testcase-container');
                testcase_container.id=`testcase-${no}`;
                testcase_container.style.display=(no===1)?'block':'none';
                testcase_container.innerHTML=`
                <div class="test-editor" >
                <div class="editor-header">${testcase.error==='compiler_error'?'Compilor Error':'Runtime Error'} </div>
                <div class="text-content" id="test-input"><pre>${testcase.error_message}</pre></div>
                </div>
                </div>`;
                final_result.innerHTML+=testcase_container.outerHTML;
            }
        }
        no++;
    });    
    if (pass===true){

        final_result_header.innerHTML=`Run Successfully! You have passed all the Sample testcases`;
    }
    else{
        final_result_header.innerHTML=`Sorry! You have failed some Sample testcases`;
    }


final_result.scrollIntoView({ behavior: "smooth",block:'end'});
}

function testcase_handling(data){
    final_result=document.getElementById('final-result');
    final_result_header=document.getElementById('final-result-header');
    final_result.innerHTML=``;
    no=1;
    pass=true;
    if (data.success==false){
        const lives=document.querySelectorAll('#lives span');
        let reds=0;
        let whites=0;
        lives.forEach( heart=> {
            const type=heart.getAttribute('heart-type');
            if (type==='red'){
                reds+=1;
            }
            else{
                whites+=1;
            }
        });
        if (reds!=0){
            const heart_to_change=lives[reds-1];
        heart_to_change.innerHTML='🩶'
        heart_to_change.setAttribute('heart-type','white');
        }
        
    }
    else{
        pass;
    }
    data.sample_testcase.forEach(testcase => {
        if (testcase.success===true ){
            final_result.innerHTML += `
            <button id="testcase-btn-${no}" class="testcase-button" 
                
                onclick="view_testcase(${no})">
                🔽 ${no} - Correct Answer 
            </button>
        `;            create_testcase_content(no,testcase.input,testcase.expected_output,testcase.actual_output);
        }
        else{
            final_result.innerHTML += `
            <button id="testcase-btn-${no}" class="testcase-button" 
                onclick="view_testcase(${no})">
                🔽 ${no} ${testcase.error} 
            </button>
        `;
        // final_result.innerHTML+=`<button  style='background:var(--bg-tertiary);cursor:pointer;border:1px solid var(--border-color);padding:10px;border-radius:5px'onclick='view_testcase(${no})''>🔓 ${no}-${testcase.error} --score:0 --View Details</button><br>`;
            pass=false;
            if (testcase.error==='wrong_answer'){
                create_testcase_content(no,testcase.input,testcase.expected_output,testcase.actual_output);
            }
            else{
                testcase_container=document.createElement('div');
                testcase_container.classList.add('testcase-container');
                testcase_container.id=`testcase-${no}`;
                testcase_container.style.display=(no===1)?'block':'none';
                testcase_container.innerHTML=`
                <div class="test-editor" >
                <div class="editor-header">${testcase.error==='compiler_error'?'Compilor Error':'Runtime Error'} </div>
                <div class="text-content" id="test-input"><pre>${testcase.error_message}</pre></div>
                </div>
                </div>`;
                final_result.innerHTML+=testcase_container.outerHTML;
            }
        }
        no++;
    });    
    
    data.hidden_testcase.forEach(testcase => {
        
        if (testcase.success===true){
            final_result.innerHTML+=`<div class='testcase-button' >&#128274; ${no}-Correct answer</div>`;
        }
        else{
            final_result.innerHTML+=`<div class='testcase-button' >&#128274; ${no}-${testcase.error}</div>`;
            pass=false;
        }
        no++;
    });
    if (pass===true){

        final_result_header.innerHTML=`Congratulations! You have passed all the testcases`;
    }
    else{

 

        

        
        final_result_header.innerHTML=`Sorry! You have failed some testcases`;
    }


final_result.scrollIntoView({ behavior: "smooth",block:'end'});
}








function create_testcase_content(number,input,expected_output,actual_output){
    const editor_container=document.getElementById('editors-container');
    testcase_container=document.createElement('div');
    testcase_container.classList.add('testcase-container');
    testcase_container.id=`testcase-${number}`;
    testcase_container.style.display=(number===1)?'block':'none';
    testcase_container.innerHTML=` 
    <div class="test-editor" >
    <div class="editor-header">Test Input </div>
    <div class="text-content" id="test-input"><pre>${input}</pre></div>
    </div>
</div>
<div class="test-editor-container" style="display: flex; flex-direction: row;">
    <div class="test-editor" style="flex: 50%;" >
        <div class="editor-header">Expected Output</div>
        <div class="text-content" style="height: 100px;" id="expected-output">
        <pre>${expected_output}</pre>
        </div>
    </div>
    <div class="test-editor" style="flex: 50%; margin-left: 5px;">
        <div class="editor-header">Actual Output</div>
        <div class="text-content" style="height: 100px;" id="actual-output">
        <pre>${actual_output===null?'Your code is not giving any output':actual_output}</pre>
        </div>
    </div>
</div>`;
// editor_container.appendChild(testcase_container);
final_result=document.getElementById('final-result');
final_result.innerHTML+=testcase_container.outerHTML;
testcase_container.scrollIntoView({ behavior: "smooth",block:'end'});
}

function view_testcase(number) {
    let testcase_container = document.getElementById(`testcase-${number}`);
    let button = document.getElementById(`testcase-btn-${number}`);
    let is_none = testcase_container.style.display === 'none';

    // Hide all other test cases
    document.querySelectorAll('.testcase-container').forEach(container => container.style.display = 'none');
    document.querySelectorAll('.testcase-button').forEach(btn => btn.innerHTML = btn.innerHTML.replace('🔼', '🔽'));

    // Toggle the current test case
    if (is_none) {
        testcase_container.style.display = 'block';
        button.innerHTML = button.innerHTML.replace('🔽', '🔼');
    } else {
        testcase_container.style.display = 'none';
        button.innerHTML = button.innerHTML.replace('🔼', '🔽');
    }

    // Scroll to the bottom of the container
    var editor_container = document.getElementById('editors-container');
    editor_container.scrollTop = editor_container.scrollHeight;
}
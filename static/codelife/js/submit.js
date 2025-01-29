function initializeSubmitButton() {
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.addEventListener('click', () => {
        submitBtn.disabled=true;
        const programCode = document.querySelector('#textarea1').value;
        const question_number = document.getElementById('question_id').dataset.questionId;
        const language=document.getElementById('language').value;
        console.log('Submitting program:', programCode);
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
        }).then(response => response.json()).then(data => {
            console.log('Submission result:', data);
            const testcase_containers=document.querySelectorAll('.testcase-container');
            testcase_containers.forEach(container => container.remove());
            testcase_handling(data);
        });
        setTimeout(() => {
            submitBtn.disabled = false;
            console.log("Button re-enabled after 10 seconds.");
        }, 10000);
        
    });
   
    
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
            final_result.innerHTML+=`<button style='background:lightblue;cursor:pointer;' onclick='view_testcase(${no})' >🔓${no}-correct answer --score:10 --View Details</button><br>`;
            create_testcase_content(no,testcase.input,testcase.expected_output,testcase.actual_output);
        }
        else{
            final_result.innerHTML+=`<button  style='background:lightblue;cursor:pointer; 'onclick='view_testcase(${no})''>🔓 ${no}-${testcase.error} --score:0 --View Details</button><br>`;
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
            final_result.innerHTML+=`🔒  ${no}-correct answer --score:10<br>`;
        }
        else{
            final_result.innerHTML+=`🔒  ${no}-${testcase.error} --score:0<br>`;
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

function view_testcase(number){
    testcase_container=document.getElementById(`testcase-${number}`);
    is_none=testcase_container.style.display==='none';
    document.querySelectorAll('.testcase-container').forEach(container => container.style.display='none');
    if(is_none){
        testcase_container.style.display='block';
    }
    else{
        testcase_container.style.display='none';
    }
    var editor_container=document.getElementById('editors-container');
    editor_container.scrollTop = editor_container.scrollHeight;
}  
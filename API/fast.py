from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import tempfile

# Create the FastAPI app
app = FastAPI()

# Enable CORS for your FastAPI app (if you're testing from a browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (adjust this for more security in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Data model to accept the code, language, and test cases
class TestCase(BaseModel):
    input_data: str
    expected_output: str
    # timelimit:float
    hidden: bool

class CodeRequest(BaseModel):
    language: str
    code: str
    timelimit:int # [python,c,cpp,java]
    testcases: list[TestCase]

# Function to execute the code based on language and test case input
def run_code(language: str, code: str, testcases: list[TestCase],timelimit:int):
    try:
        # Create a temporary directory to store code and output files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = ""
            output_name = ""
            compile_cmd = []
            run_cmd = []
            # Save code to a temporary file
            if language == "c":
                file_name = os.path.join(temp_dir, "program.c")
                output_name = os.path.join(temp_dir, "program.out")
                compile_cmd = ["gcc", file_name, "-o", output_name]
                run_cmd = [output_name]
                # timelimit=timelimits[1]
            elif language == "cpp":
                file_name = os.path.join(temp_dir, "program.cpp")
                output_name = os.path.join(temp_dir, "program.out")
                compile_cmd = ["g++", file_name, "-o", output_name]
                run_cmd = [output_name]
                # timelimit=timelimits[2]
            elif language == "java":
                file_name = os.path.join(temp_dir, "Main.java")
                output_name = os.path.join(temp_dir, "Main")
                compile_cmd = ["javac", file_name]
                run_cmd = ["java", "-cp", temp_dir, "Main"]
                # timelimit=timelimits[3]
            elif language == 'python':
                file_name = os.path.join(temp_dir, "example.py")
                run_cmd=['python',file_name]
                # timelimit=timelimits[0]
            else:
                raise HTTPException(status_code=400, detail="Unsupported language")

            # Write the code to the temporary file
            with open(file_name, "w") as f:
                f.write(code)
            print(f"Code written to {file_name}:\n{code}")  # Debug: print the code
            
            # Compile the code
            if language!='python':
                
                compile_process = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if compile_process.returncode != 0:
                    # Capture the compilation error and return as a 400 error
                    error_message = compile_process.stderr.decode()
                    print(f"Compilation Error: {error_message}")  # Debug: print the error message
                    return {'success':False,'error':'compilation_error','error_message':error_message},[]
                    # raise HTTPException(status_code=400, detail=f"Compilation Error: {error_message}")
            # Run the compiled code for each test case
            hidden = []
            sample=[]
            print(testcases)
            for i,testcase in enumerate(testcases): 
                try:
                    run_process = subprocess.run(
                    run_cmd,
                    input=testcase.input_data.encode(),  
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=timelimit,
                    )
                except subprocess.TimeoutExpired:
                    if testcase.hidden==False:
                        sample.append({'success':False,'error':'time_limit_exceeded','error_message':'Time Limit Exceeded'})
                    else:
                        hidden.append({'success':False, "error":'time_limit_exceeded'})
                    continue
                if run_process.returncode != 0:
                    # Capture runtime errors for this test case
                    error_message = run_process.stderr.decode()
                    print(f"Runtime Error: {error_message}")  # Debug: print the error message
                    if testcase.hidden==False:
                        sample.append({'success':False,'error':'runtime_error','error_message':error_message})
                    else:
                        hidden.append({'success':False, "error":'runtime_error'})
                else:
                    output = run_process.stdout.decode() 
                    if output.strip() != testcase.expected_output.strip():
                        if output:
                            output=output.strip()
                        else:
                            output=None
                        if testcase.hidden==False:
                            sample.append({'success':False,'error':'wrong_answer','input':testcase.input_data.strip(),'expected_output':testcase.expected_output.strip(),'actual_output':output})
                            # print(f"Expected Output: {testcase.expected_output.strip()}")
                            # print(f"Your Output: {output}")
                        else:
                            hidden.append({'success':False,"error":'wrong_answer'})
                        # print(f"Wrong Answer: {output}")
                    else:
                        if testcase.hidden==False:
                            sample.append({'success':True,'error':None,'input':testcase.input_data.strip(),'expected_output':testcase.expected_output.strip(),'actual_output':output.strip()})
                        else:
                            hidden.append({'success':True, "error": None})
            return sample,hidden

    except HTTPException as http_err:
        # If a specific HTTP exception was raised, forward it
        raise http_err

    except Exception as e:
        # Catch unexpected errors and raise a 500 server error
        print(f"Unexpected Error: {e}")  # Debug: print unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Endpoint to run the code
@app.post("/run/")
async def run_program(code_request: CodeRequest):
    sample_testcase,hidden_testcase = run_code(code_request.language, code_request.code, code_request.testcases,code_request.timelimit)
    # print(sample_testcase)
    return {'sample_testcase':sample_testcase,"hidden_testcase": hidden_testcase}
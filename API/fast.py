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

class CodeRequest(BaseModel):
    language: str
    code: str
    testcases: list[TestCase]

# Function to execute the code based on language and test case input
def run_code(language: str, code: str, testcases: list[TestCase]):
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

            elif language == "cpp":
                file_name = os.path.join(temp_dir, "program.cpp")
                output_name = os.path.join(temp_dir, "program.out")
                compile_cmd = ["g++", file_name, "-o", output_name]
                run_cmd = [output_name]

            elif language == "java":
                file_name = os.path.join(temp_dir, "Main.java")
                output_name = os.path.join(temp_dir, "Main")
                compile_cmd = ["javac", file_name]
                run_cmd = ["java", "-cp", temp_dir, "Main"]
            elif language == 'python':
                file_name = os.path.join(temp_dir, "example.py")
                run_cmd=['python',file_name]
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
            results = []
            for i,testcase in enumerate(testcases):
                run_process = subprocess.run(
                    run_cmd,
                    input=testcase.input_data.encode(),  # Pass input to the program
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if run_process.returncode != 0:
                    # Capture runtime errors for this test case
                    error_message = run_process.stderr.decode()
                    print(f"Runtime Error: {error_message}")  # Debug: print the error message
                    if i==0:
                        sample_testcase={'success':False,'error':'runtime_error','error_message':error_message}
                        break
                    results.append({'success':False, "error":'runtime_error','error_message':error_message})
                    break
                else:
                    output = run_process.stdout.decode()
                    if output.strip() != testcase.expected_output.strip():
                        # Capture wrong answers for this test case
                        if i==0:
                            print(f"Expected Output: {testcase.expected_output.strip()}")
                            print(f"Your Output: {output.strip()}")
                            sample_testcase={'success':False,'error':'wrong_answer','your output':output.strip()}
                            break
                        print(f"Wrong Answer: {output.strip()}")
                        results.append({'success':False,"error":'wrong_answer'})
                        break
                    else:
                        if i==0:
                            sample_testcase={'success':True,'error':None}
                        results.append({'success':True, "error": None})
            return sample_testcase,results

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
    sample_testcase,hidden_testcase = run_code(code_request.language, code_request.code, code_request.testcases)
    return {'sample_testcase':sample_testcase,"hidden_testcase": hidden_testcase}
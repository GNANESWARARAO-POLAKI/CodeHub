from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import tempfile
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS settings (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestCase(BaseModel):
    input_data: str
    expected_output: str
    hidden: bool

class CodeRequest(BaseModel):
    language: str
    code: str
    timelimit: int
    testcases: list[TestCase]

executor = ThreadPoolExecutor(max_workers=5)

def run_code(language: str, code: str, testcases: list[TestCase], timelimit: int):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = ""
            compile_cmd = []
            run_cmd = []

            # Set file names and commands based on language
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
                compile_cmd = ["javac", file_name]
                run_cmd = ["java", "-cp", temp_dir, "Main"]
            elif language == "python":
                file_name = os.path.join(temp_dir, "script.py")
                run_cmd = ["python", file_name]
            else:
                raise HTTPException(status_code=400, detail="Unsupported language")

            # Write the code to the temporary file
            with open(file_name, "w") as f:
                f.write(code)

            # Compile the code if necessary
            if language in ["c", "cpp", "java"]:
                compile_process = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if compile_process.returncode != 0:
                    error_message = compile_process.stderr.decode()
                    logger.error(f"Compilation Error: {error_message}")
                    return {"success": False, "error": "compilation_error", "message": error_message}, []

            # Run the compiled or interpreted code for each test case
            sample_results = []
            hidden_results = []

            for testcase in testcases:
                try:
                    run_process = subprocess.run(
                        run_cmd,
                        input=testcase.input_data.encode(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=timelimit
                    )
                except subprocess.TimeoutExpired:
                    if not testcase.hidden:
                        sample_results.append({"success": False, "error": "time_limit_exceeded"})
                    else:
                        hidden_results.append({"success": False, "error": "time_limit_exceeded"})
                    continue

                if run_process.returncode != 0:
                    error_message = run_process.stderr.decode()
                    logger.error(f"Runtime Error: {error_message}")
                    if not testcase.hidden:
                        sample_results.append({"success": False, "error": "runtime_error", "message": error_message})
                    else:
                        hidden_results.append({"success": False, "error": "runtime_error"})
                else:
                    output = run_process.stdout.decode().strip()
                    expected_output = testcase.expected_output.strip()
                    if output != expected_output:
                        if not testcase.hidden:
                            sample_results.append({
                                "success": False,
                                "error": "wrong_answer",
                                "input": testcase.input_data,
                                "expected": expected_output,
                                "actual": output
                            })
                        else:
                            hidden_results.append({"success": False, "error": "wrong_answer"})
                    else:
                        if not testcase.hidden:
                            sample_results.append({"success": True})
                        else:
                            hidden_results.append({"success": True})

            return sample_results, hidden_results

    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/run/")
async def run_program(code_request: CodeRequest):
    loop = asyncio.get_event_loop()
    sample, hidden = await loop.run_in_executor(executor, run_code, code_request.language, code_request.code, code_request.testcases, code_request.timelimit)
    return {"sample_testcase": sample, "hidden_testcase": hidden}

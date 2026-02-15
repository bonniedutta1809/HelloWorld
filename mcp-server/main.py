import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

# ✅ Check API key properly
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY not set. Run:\n"
        "export OPENAI_API_KEY='sk-...'\n"
        "Then restart the server."
    )

client = OpenAI(api_key=api_key)


@app.post("/generate-tests")
async def generate_tests(request: Request):
    try:
        data = await request.json()
        print("Received request:", data)

        # ✅ Build absolute base directory
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Java file location (adjust if needed)
        java_file_path = os.path.join(BASE_DIR, "HelloWorld","src", "HelloWorld.java")
        print("Looking for file at:", java_file_path)

        # ✅ Read Java file
        with open(java_file_path, "r") as f:
            java_code = f.read()

        # ✅ Build prompt
        prompt = f"""
Generate JUnit 5 test cases for the following Java class.
Only output valid compilable Java test code.

{java_code}
"""

        # ✅ Call LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        test_code = response.choices[0].message.content

        # ✅ Create tests folder if it doesn't exist
        tests_dir = os.path.join(BASE_DIR, "tests")
        os.makedirs(tests_dir, exist_ok=True)

        output_path = os.path.join(tests_dir, "HelloWorldTest.java")

        # ✅ Save generated test
        with open(output_path, "w") as f:
            f.write(test_code)

        print("Test file saved at:", output_path)

        return {
            "status": "success",
            "message": "Test file generated",
            "output_file": output_path
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}

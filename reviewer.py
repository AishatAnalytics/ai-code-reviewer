import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic
import time

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def read_code_files(directory):
    print(f"Reading code files from {directory}...")
    files = []
    
    for filename in os.listdir(directory):
        if filename.endswith(('.py', '.js', '.ts', '.java')):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            files.append({
                'filename': filename,
                'content': content,
                'lines': len(content.split('\n'))
            })
            print(f"Read {filename} ({len(content.split(chr(10)))} lines)")
    
    return files

def review_code(files):
    print(f"\nSending {len(files)} file(s) to Claude for review...")
    
    code_content = "\n\n".join([
        f"--- FILE: {f['filename']} ---\n{f['content']}"
        for f in files
    ])
    
    prompt = f"""
You are a senior software engineer and security expert conducting a thorough code review.

Review the following code and provide:

1. SECURITY ISSUES (Critical, High, Medium, Low severity)
   - SQL injection vulnerabilities
   - Hardcoded credentials
   - Exposed API keys
   - Input validation issues

2. CODE QUALITY ISSUES
   - Error handling gaps
   - Performance problems
   - Missing best practices

3. AWS BEST PRACTICES
   - IAM and permissions issues
   - Resource configuration problems

4. SPECIFIC FIXES
   - For each issue provide the exact fixed code

5. OVERALL SCORE out of 100
   - Security score
   - Code quality score
   - AWS best practices score

CODE TO REVIEW:
{code_content}

Format your response clearly with sections and severity levels.
Be specific and actionable. Include fixed code examples.
Avoid using emojis in your response.
    """
    
    for attempt in range(3):
        try:
            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                print("Retrying in 5 seconds...")
                time.sleep(5)
    
    return "Code review unavailable — API temporarily down."

def generate_report(files, review):
    report = {
        'timestamp': datetime.now().isoformat(),
        'files_reviewed': [f['filename'] for f in files],
        'total_lines': sum(f['lines'] for f in files),
        'review': review
    }
    
    with open('code_review_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    with open('code_review_report.md', 'w', encoding='utf-8') as f:
        f.write(f"# Code Review Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Files Reviewed:** {', '.join([f['filename'] for f in files])}\n\n")
        f.write(f"**Total Lines:** {sum(f['lines'] for f in files)}\n\n")
        f.write(f"---\n\n")
        f.write(review)
    
    print("\nReports saved:")
    print("   - code_review_report.json")
    print("   - code_review_report.md")

def run():
    print("AI Code Reviewer")
    print("=================\n")
    
    print("Step 1: Reading code files...")
    files = read_code_files('./sample_code')
    
    if not files:
        print("No code files found!")
        return
    
    print(f"\nFound {len(files)} file(s) to review")
    
    print("\nStep 2: Running AI code review...")
    review = review_code(files)
    
    print("\n" + "="*50)
    print("CLAUDE CODE REVIEW")
    print("="*50 + "\n")
    print(review)
    
    print("\nStep 3: Generating reports...")
    generate_report(files, review)
    
    print("\nAI Code Review complete!")

if __name__ == "__main__":
    run()
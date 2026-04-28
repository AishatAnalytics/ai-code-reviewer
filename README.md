# AI Code Reviewer

AI powered code reviewer that scans for security vulnerabilities and AWS best practices using Claude.

## The Problem
Developers push code with security vulnerabilities, hardcoded credentials and SQL injection risks. Manual code reviews miss issues. This automates security scanning before code reaches production.

## What It Does
- Reads all Python and JavaScript files in a directory
- Sends code to Claude AI for expert security review
- Detects SQL injection vulnerabilities
- Flags hardcoded credentials and API keys
- Identifies missing input validation
- Checks AWS best practices
- Generates detailed markdown and JSON reports with fixed code examples

## Sample Findings
CRITICAL: SQL injection vulnerability in get_user function
CRITICAL: Hardcoded AWS credentials in upload_to_s3 function
CRITICAL: Hardcoded database password
HIGH: Missing input validation in process_payment function
HIGH: No error handling in lambda_handler

## Overall Scores
Security Score: 15/100
Code Quality Score: 40/100
AWS Best Practices Score: 20/100

## Tech Stack
- Python 3
- Claude API (Anthropic)

## Key Concepts Demonstrated
- Shift left security
- Automated code review
- OWASP vulnerability detection
- AWS Well-Architected Security Pillar

## How To Run
- Clone the repo
- pip install anthropic python-dotenv
- Add your ANTHROPIC_API_KEY to .env
- Put your code files in the sample_code folder
- Run py reviewer.py

## Part of my 30 cloud projects in 30 days series
Follow along: https://www.linkedin.com/in/aishatolatunji/
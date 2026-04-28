import boto3
import json
import mysql.connector

# Database connection
db = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="password123",
  database="myapp"
)

def get_user(user_id):
    cursor = db.cursor()
    # Potential SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client('s3',
        aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
        aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    )
    s3.upload_file(file_path, bucket_name, file_path)

def process_payment(amount, card_number):
    # No input validation
    print(f"Processing payment of {amount} for card {card_number}")
    return True

def lambda_handler(event, context):
    user_id = event['user_id']
    user = get_user(user_id)
    
    # No error handling
    data = json.loads(event['data'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }
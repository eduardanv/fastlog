# cloudwatch.py
import boto3
import logging
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

# Configuração do cliente boto3
cloudwatch_logs = boto3.client('logs', region_name='us-east-1')  # Substitua pela sua região, se necessário

log_group_name = '/aws/ec2/application'  # Nome do grupo de logs no CloudWatch
log_stream_name = 'EC2-Logs'  # Nome do stream de logs

def create_log_group_and_stream():
    try:
        # Verifica se o grupo de logs já existe, caso contrário, cria um novo
        cloudwatch_logs.create_log_group(logGroupName=log_group_name)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        print(f"Log group '{log_group_name}' já existe.")
    
    try:
        # Cria o log stream se não existir
        cloudwatch_logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        print(f"Log stream '{log_stream_name}' já existe.")

def send_log_to_cloudwatch(message):
    try:
        # Obtemos o timestamp atual para registrar a data e hora do log
        timestamp = int(round(time.time() * 1000))
        
        # Envia o log para o CloudWatch Logs
        response = cloudwatch_logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        )
        print("Log enviado para o CloudWatch:", response)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Erro de credenciais: {e}")
    except Exception as e:
        print(f"Erro ao enviar log para o CloudWatch: {e}")

import requests
import csv
from io import StringIO
import boto3
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    """
    Função Lambda para extrair dados de websites e armazenar no S3,
    processando apenas as 500 primeiras linhas.
    """
    s3 = boto3.client('s3')
    bucket_name = 's3-raw-lab-tracksecure'  # Substitua pelo nome do seu bucket S3

    try:
        url ="https://transparencia.metrosp.com.br/sites/default/files/Entrada%20de%20Passageiros%20por%20Esta%C3%A7%C3%A3o%20-%20M%C3%A9dia%20Dias%20%C3%9Ateis%20-%202024_4.csv"
        response = requests.get(url)
        response.raise_for_status()


        s3.put_object(Bucket=bucket_name, Key='dados_metro.csv', Body=response.content)

        print("Dados armazenados com sucesso no S3!")
        return {
            'statusCode': 200,
            'body': 'Dados extraídos e armazenados no S3 com sucesso!'
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return {
            'statusCode': 500,
            'body': f"Erro na requisição: {e}"
        }
    except Exception as e:
        print(f"Erro ao processar os dados ou armazenar no S3: {e}")
        return {
            'statusCode': 500,
            'body': f"Erro ao processar os dados ou armazenar no S3: {e}"
        }
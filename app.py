from chalice import Chalice
from openai import OpenAI
import boto3
import json

app = Chalice(app_name='lambda-poetry')

secrets_client = boto3.client('secretsmanager')

def get_openai_api_key():
    secret_name = "openai-key"
    region_name = "us-east-1"

    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret['OPENAI_API_KEY']

@app.route('/')
def generate_poetry():
    try:
        # openai.api_key = get_openai_api_key()
        client = OpenAI(api_key=get_openai_api_key())

        keywords = ["nature", "dream", "freedom"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Você é um poeta do estilo cordel. Seu trabalho é criar um poema usando 3 palavras-chave.
                 Crie duas estrofes de 5 linhas. Responda em português."""},
                {
                    "role": "user",
                    "content": str(", ".join(keywords))
                }
            ],
            temperature=0.7,
            max_tokens=100
        )

        # Retorna a poesia gerada
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}
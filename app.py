from flask import Flask, render_template, send_file, request
import os
import requests
from PIL import Image
import json
from openai import AzureOpenAI

app = Flask(__name__)

# Azure OpenAI 설정
client = AzureOpenAI(
    api_version="2023-12-01-preview",
    api_key="e09fbd39e4704995859a65c52cd9a3b7",  # Azure API Key로 변경
    azure_endpoint="https://aoaiweb.openai.azure.com/"  # Azure Endpoint로 변경
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # 프론트엔드에서 받은 프롬프트를 활용하여 이미지 생성
    prompt = request.form.get('prompt')
    meta_prompt = f"""
    You are an assistant designer that creates images for children.
    The image needs to be safe for work and appropriate for children.
    The image needs to be in color.
    The image needs to be in landscape orientation.
    The image needs to be in a 16:9 aspect ratio.
    """
    full_prompt = meta_prompt + prompt

    result = client.images.generate(
        model="dalle3",
        prompt=full_prompt,
        n=1
    )

    json_response = json.loads(result.model_dump_json())
    image_url = json_response["data"][0]["url"]  # 이미지 URL 추출

    # 이미지 다운로드 및 저장
    image_dir = os.path.join(os.curdir, 'static', 'images')
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    image_path = os.path.join(image_dir, 'generated_image.png')
    generated_image = requests.get(image_url).content
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    # 생성된 이미지를 표시하기 위해 이미지 경로를 반환
    return render_template('index.html', image_path='images/generated_image.png')

if __name__ == '__main__':
    app.run(debug=True)

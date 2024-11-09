import torch
import pandas as pd
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from flask import Flask, request, jsonify, make_response
import requests
app = Flask(__name__)
MODEL_NAME = "IlyaGusev/saiga_mistral_7b"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"
DEFAULT_SYSTEM_PROMPT = "<s>system\nТы бот, который заполняет характеристики товара на основе его названия. Отвечай кратко одним словом или цифрой, давай ответы только по конкретной характеристике. Если данную характеристику нельзя получить из названия, отвечай 'None'.</s>"
prompt = """<s>system\nТы бот, который заполняет характеристики товара на основе его названия. Отвечай кратко одним словом или цифрой, давай ответы только по конкретной характеристике. Если данную характеристику нельзя получить из названия, отвечай 'None'.</s>
<user>Спарси html и достань оттуда ключевые характеристикиHTML:</user><bot>"
"""
config = PeftConfig.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="cuda:0"
)
model = PeftModel.from_pretrained(
    model,
    MODEL_NAME,
    torch_dtype=torch.float16
)
def generate(model, tokenizer, prompt, generation_config):
    data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(
        **data,
        generation_config=generation_config
    )[0]
    output_ids = output_ids[len(data["input_ids"][0]):]
    output = tokenizer.decode(output_ids, skip_special_tokens=True)
    return output.strip()

@app.route('/generate_characteristics', methods=['POST'])
def generate_characteristics():
    data = request.get_json()
    properties = data['properties']
    product_name = data['name']
    

    characteristics = [item["name"] for item in properties]
    id_characteristics = [item["id"] for item in properties]
    
    parser_url = 'https://zakupki-api.kovalev.team/api/v1/ste/ste_name=?{product_name}'
    response = requests.get(parser_url)
    html = response.json()['data']

    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    generation_config = GenerationConfig.from_pretrained(MODEL_NAME, temperature=0.0001, max_new_tokens=10)
    
    prompt = DEFAULT_SYSTEM_PROMPT + "\n" + "<s>user\nНазвание товара:" + product_name + "html:" + html + "\nХарактеристика:\n"
    result_df = pd.DataFrame(columns=['id', 'characteristics', 'value'])
    for i, char in enumerate(characteristics):
        full_prompt = prompt + char + "<s>bot"
        output = generate(model, tokenizer, full_prompt, generation_config)
        result_df = pd.concat([result_df, pd.DataFrame({'id': [id_characteristics[i]], 'characteristics': [str(char)], 'value': [str(output)]})], ignore_index=True)
    response = make_response(jsonify(result_df.to_dict(orient='records')))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5001)
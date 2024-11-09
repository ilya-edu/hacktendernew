from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np
import os

app = Flask(__name__)

model = SentenceTransformer("cointegrated_LaBSE-en-ru")

@app.route("/encode", methods=["POST"])
def encode():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Encode the text
        encoded_text = model.encode(text, convert_to_tensor=True)
        # Convert tensor to list to make it serializable
        np_vector = encoded_text.cpu().detach().numpy()
        min_non_zero = np.min(np.abs(np_vector[np.nonzero(np_vector)]))
        max_decimals = len(str(min_non_zero).split('.')[-1])
        array_str = ",".join([f"{x:.{max_decimals}f}" for x in np_vector])
        formatted_str = f"{{{array_str}}}"
        return formatted_str
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# from flask import Flask, request, jsonify, send_from_directory
# from ultralytics import YOLO
# from gensim.models.fasttext import FastText
# from flask_cors import CORS
# import pandas as pd
# import numpy as np
# from PIL import Image
# import os
# import uuid
# import re
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# CORS(app)
# app.config['UPLOAD_FOLDER'] = 'static'


# yolo_model = YOLO("best.pt")
# fasttext_model = FastText.load("fasttext_model.bin")


# def clean_ingredients(text):
#     if not isinstance(text, str):
#         return []
#     text = text.lower().strip()

#     composite_phrases = [
#         'bawang merah', 'bawang putih', 'bawang bombay', 'cabai rawit', 'daun bawang',
#         'jeruk nipis', 'kecap manis', 'merica bubuk', 'minyak goreng', 'santan kelapa'
#     ]
#     for phrase in composite_phrases:
#         text = re.sub(rf'\b{phrase}\b', phrase.replace(' ', '_'), text)

#     text = re.sub(r'\([^)]*\)', '', text)
#     text = re.sub(r'[^\w\s_]', ' ', text)
#     text = re.sub(r'\d+[\s\/]*\d*', '', text)

#     units = [
#         'sdm', 'sdt', 'sendok', 'gelas', 'ml', 'liter', 'gr', 'kg',
#         'ons', 'ekor', 'buah', 'butir', 'batang', 'lembar', 'ikat',
#         'sedikit','selera','gram','secukupnya','siung','siaung','besar','kecil'
#     ]
#     text = re.sub(rf'\b(?:{"|".join(units)})\b', '', text)

#     cooking_verbs = [
#         'potong', 'iris', 'masak', 'cuci', 'haluskan', 'goreng',
#         'tumis', 'campur', 'kupas', 'rebus', 'panggang', 'kocok',
#         'parut', 'cincang', 'aduk', 'tambahkan', 'ambil', 'siapkan',
#         'gunakan', 'panaskan', 'hidangkan', 'tuang', 'taburkan',
#         'masukkan', 'peras', 'rendam', 'tiriskan', 'bahan', 'bh'
#     ]
#     text = re.sub(rf'\b(?:{"|".join(cooking_verbs)})\b', '', text)

#     for sep in [',', ';', '/', '&', 'dan', '+']:
#         text = text.replace(sep, ' ')

#     tokens = []
#     for token in text.split():
#         token = token.replace('_', ' ')
#         if token.strip() and len(token) > 1:
#             tokens.append(token)

#     return list(dict.fromkeys(tokens))


# def get_mean_vector(tokens):
#     vectors = [fasttext_model.wv[token] for token in tokens if token in fasttext_model.wv]
#     if vectors:
#         return np.mean(vectors, axis=0)
#     else:
#         return np.zeros(fasttext_model.vector_size)


# recipes = pd.read_csv("recipes.csv")
# recipes['ingredients_clean'] = recipes['Ingredients'].fillna('').astype(str).str.lower()
# recipes['tokens'] = recipes['ingredients_clean'].apply(clean_ingredients)
# recipes['vector'] = recipes['tokens'].apply(get_mean_vector)
# recipe_vectors = np.vstack(recipes['vector'].to_numpy())


# @app.route("/detect", methods=["POST"])
# def detect():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files['image']
#     unique_id = str(uuid.uuid4())
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.jpg")
#     image_file.save(image_path)

#     results = yolo_model(image_path)
#     names = yolo_model.names
#     ingredients = list(set([names[int(box.cls)] for box in results[0].boxes]))

#     result_img = results[0].plot()
#     detected_path = os.path.join(app.config['UPLOAD_FOLDER'], f"detected_{unique_id}.jpg")
#     Image.fromarray(result_img).save(detected_path)

#     return jsonify({
#         "ingredients": ingredients,
#         "image_url": f"/static/detected_{unique_id}.jpg"
#     })


# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.get_json()
#     ingredients = data.get("ingredients", [])
#     if not ingredients:
#         return jsonify({"error": "No ingredients provided"}), 400

#     cleaned = clean_ingredients(" ".join(ingredients))
#     vector = get_mean_vector(cleaned).reshape(1, -1)
#     similarities = cosine_similarity(vector, recipe_vectors)[0]
#     top_indices = similarities.argsort()[-10:][::-1]

#     BASE_URL = "https://cookpad.com"

#     recommendations = recipes.iloc[top_indices][['Title', 'Ingredients', 'Loves', 'URL','tokens']].copy()
#     recommendations['URL'] = BASE_URL + recommendations['URL'].fillna("").astype(str)
#     recommendations['score'] = similarities[top_indices]

#     return jsonify({
#         "recommendations": recommendations.to_dict(orient="records")
#     })

# @app.route("/static/<filename>")
# def serve_static(filename):
#     return send_from_directory("static", filename)

# if __name__ == "__main__":
#     app.run(debug=True)
# from flask import Flask, request, jsonify, send_from_directory
# from ultralytics import YOLO
# from gensim.models.fasttext import FastText
# from flask_cors import CORS
# import pandas as pd
# import numpy as np
# from PIL import Image
# import os
# import uuid
# import re
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# CORS(app)
# app.config['UPLOAD_FOLDER'] = 'static'

# # Load model YOLO dan FastText
# yolo_model = YOLO("best.pt")
# fasttext_model = FastText.load("fasttext_model.bin")

# # Daftar kelas bahan yang diperbolehkan
# allowed_ingredients = [
#     "kangkung", "bayam", "brokoli", "bawang merah", "bawang putih",
#     "cabai", "tomat", "salam", "wortel", "kubis",
#     "terong", "buncis", "daun bawang", "ayam", "sapi",
#     "jahe", "kunyit", "tahu", "tempe", "telur"
# ]

# # Preprocessing dataset resep
# def clean_ingredients(text):
#     if not isinstance(text, str):
#         return []
#     text = text.lower().strip()

#     composite_phrases = [
#         'bawang merah', 'bawang putih', 'cabai rawit', 'daun bawang',
#         'jeruk nipis', 'kecap manis', 'merica bubuk', 'minyak goreng', 'santan kelapa'
#     ]
#     for phrase in composite_phrases:
#         text = re.sub(rf'\b{phrase}\b', phrase.replace(' ', '_'), text)

#     text = re.sub(r'\([^)]*\)', '', text)
#     text = re.sub(r'[^\w\s_]', ' ', text)
#     text = re.sub(r'\d+[\s\/]*\d*', '', text)

#     units = [
#         'sdm', 'sdt', 'sendok', 'gelas', 'ml', 'liter', 'gr', 'kg',
#         'ons', 'ekor', 'buah', 'butir', 'batang', 'lembar', 'ikat',
#         'sedikit', 'selera', 'gram', 'secukupnya', 'siung', 'siaung', 'besar', 'kecil'
#     ]
#     text = re.sub(rf'\b(?:{"|".join(units)})\b', '', text)

#     cooking_verbs = [
#         'potong', 'iris', 'masak', 'cuci', 'haluskan', 'goreng',
#         'tumis', 'campur', 'kupas', 'rebus', 'panggang', 'kocok',
#         'parut', 'cincang', 'aduk', 'tambahkan', 'ambil', 'siapkan',
#         'gunakan', 'panaskan', 'hidangkan', 'tuang', 'taburkan',
#         'masukkan', 'peras', 'rendam', 'tiriskan', 'bahan', 'bh'
#     ]
#     text = re.sub(rf'\b(?:{"|".join(cooking_verbs)})\b', '', text)

#     for sep in [',', ';', '/', '&', 'dan', '+']:
#         text = text.replace(sep, ' ')

#     tokens = []
#     for token in text.split():
#         token = token.replace('_', ' ')
#         if token.strip() and len(token) > 1:
#             tokens.append(token)

#     return list(dict.fromkeys(tokens))

# def get_mean_vector(tokens):
#     vectors = [fasttext_model.wv[token] for token in tokens if token in fasttext_model.wv]
#     if vectors:
#         return np.mean(vectors, axis=0)
#     else:
#         return np.zeros(fasttext_model.vector_size)

# # Load dataset resep
# recipes = pd.read_csv("recipes.csv")
# recipes['ingredients_clean'] = recipes['Ingredients'].fillna('').astype(str).str.lower()
# recipes['tokens'] = recipes['ingredients_clean'].apply(clean_ingredients)
# recipes['vector'] = recipes['tokens'].apply(get_mean_vector)
# recipe_vectors = np.vstack(recipes['vector'].to_numpy())

# @app.route("/detect", methods=["POST"])
# def detect():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files['image']
#     unique_id = str(uuid.uuid4())
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.jpg")
#     image_file.save(image_path)

#     results = yolo_model(image_path)
#     names = yolo_model.names
#     detected_ingredients = list(set([names[int(box.cls)] for box in results[0].boxes]))

#     valid_ingredients = [b for b in detected_ingredients if b.lower() in allowed_ingredients]

#     result_img = results[0].plot()
#     detected_path = os.path.join(app.config['UPLOAD_FOLDER'], f"detected_{unique_id}.jpg")
#     Image.fromarray(result_img).save(detected_path)

#     if not valid_ingredients:
#         return jsonify({
#             "ingredients": [],
#             "message": "Bahan belum tersedia dalam sistem.",
#             "image_url": f"/static/detected_{unique_id}.jpg"
#         })

#     return jsonify({
#         "ingredients": valid_ingredients,
#         "image_url": f"/static/detected_{unique_id}.jpg"
#     })

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.get_json()
#     ingredients = data.get("ingredients", [])
#     if not ingredients:
#         return jsonify({"error": "No ingredients provided"}), 400

#     cleaned = clean_ingredients(" ".join(ingredients))
#     vector = get_mean_vector(cleaned).reshape(1, -1)
#     similarities = cosine_similarity(vector, recipe_vectors)[0]

#     BASE_URL = "https://cookpad.com"

#     def contains_any(row_tokens, input_tokens):
#         return any(token in row_tokens for token in input_tokens)

#     filtered_recipes = recipes[recipes['tokens'].apply(lambda x: contains_any(x, cleaned))].copy()

#     if filtered_recipes.empty:
#         return jsonify({"recommendations": [], "message": "Tidak ada resep yang sesuai dengan bahan yang terdeteksi."})

#     filtered_vectors = np.vstack(filtered_recipes['vector'].to_numpy())
#     filtered_similarities = cosine_similarity(vector, filtered_vectors)[0]
#     top_indices = filtered_similarities.argsort()[-10:][::-1]

#     recommendations = filtered_recipes.iloc[top_indices][['Title', 'Ingredients', 'Loves', 'URL']].copy()
#     recommendations['URL'] = BASE_URL + recommendations['URL'].fillna("").astype(str)
#     recommendations['score'] = filtered_similarities[top_indices]

#     return jsonify({
#         "recommendations": recommendations.to_dict(orient="records")
#     })

# @app.route("/static/<filename>")
# def serve_static(filename):
#     return send_from_directory("static", filename)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
from gensim.models.fasttext import FastText
import pandas as pd
import numpy as np
from PIL import Image
import os
import uuid
import re
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static'

# Load model YOLO dan FastText
yolo_model = YOLO("best.pt")
fasttext_model = FastText.load("fasttext_model.bin")

# Preprocess
ALLOWED_INGREDIENTS = [
    "kangkung", "bayam", "brokoli", "bawang merah", "bawang putih",
    "cabai", "tomat", "salam", "wortel", "kubis", "terong", "buncis",
    "daun bawang", "ayam", "sapi", "jahe", "kunyit", "tahu", "tempe", "telur"
]

# Clean Ingredients Function
def clean_ingredients(text):
    if not isinstance(text, str): return []
    text = text.lower().strip()

    composite_phrases = ["bawang merah", "bawang putih", "cabai rawit", "daun bawang"]
    for phrase in composite_phrases:
        text = re.sub(rf'\b{phrase}\b', phrase.replace(' ', '_'), text)

    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[^\w\s_]', ' ', text)
    text = re.sub(r'\d+[\s\/]*\d*', '', text)

    units = ["sdm", "sdt", "sendok", "gram", "ml", "kg", "ons", "buah", "butir", "batang", "lembar"]
    text = re.sub(rf'\b(?:{"|".join(units)})\b', '', text)

    verbs = ["potong", "iris", "masak", "tumis", "cincang", "campur", "haluskan"]
    text = re.sub(rf'\b(?:{"|".join(verbs)})\b', '', text)

    for sep in [",", ";", "/", "&", "dan", "+"]:
        text = text.replace(sep, ' ')

    tokens = []
    for token in text.split():
        token = token.replace('_', ' ')
        if token and len(token) > 1:
            tokens.append(token)

    return list(dict.fromkeys(tokens))

def get_mean_vector(tokens):
    vectors = [fasttext_model.wv[token] for token in tokens if token in fasttext_model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(fasttext_model.vector_size)

# Load Dataset
recipes = pd.read_csv("recipes.csv")
recipes['ingredients_clean'] = recipes['Ingredients'].fillna('').astype(str).str.lower()
recipes['Category'] = recipes['Category'].fillna('').astype(str)
recipes['tokens'] = recipes['ingredients_clean'].apply(clean_ingredients)
recipes['vector'] = recipes['tokens'].apply(get_mean_vector)
recipe_vectors = np.vstack(recipes['vector'].to_numpy())

# @app.route("/detect", methods=["POST"])
# def detect():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files['image']
#     unique_id = str(uuid.uuid4())
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.jpg")
#     image_file.save(image_path)

#     results = yolo_model(image_path)
#     names = yolo_model.names
#     detected = list(set([names[int(box.cls)] for box in results[0].boxes]))
#     valid_ingredients = [i for i in detected if i.lower() in ALLOWED_INGREDIENTS]

#     result_img = results[0].plot()
#     detected_path = os.path.join(app.config['UPLOAD_FOLDER'], f"detected_{unique_id}.jpg")
#     Image.fromarray(result_img).save(detected_path)

#     return jsonify({
#         "ingredients": valid_ingredients,
#         "image_url": f"/static/detected_{unique_id}.jpg"
#     })
@app.route("/detect", methods=["POST"])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    unique_id = str(uuid.uuid4())
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.jpg")
    image_file.save(image_path)

    results = yolo_model(image_path)
    names = yolo_model.names

    boxes = results[0].boxes
    detected = []
    for box in boxes:
        if box.conf[0] >= 0.5:
            cls_id = int(box.cls[0])
            name = names[cls_id]
            detected.append(name)

    detected = list(set(detected))
    valid_ingredients = [i for i in detected if i.lower() in ALLOWED_INGREDIENTS]

    result_img = results[0].plot()
    detected_path = os.path.join(app.config['UPLOAD_FOLDER'], f"detected_{unique_id}.jpg")
    Image.fromarray(result_img).save(detected_path)

    return jsonify({
        "ingredients": valid_ingredients,
        "image_url": f"/static/detected_{unique_id}.jpg"
    })

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.get_json()
#     ingredients = data.get("ingredients", [])
#     category_filter = data.get("category", "").strip().lower()

#     if not ingredients:
#         return jsonify({"error": "No ingredients provided"}), 400

#     cleaned = clean_ingredients(" ".join(ingredients))
#     vector = get_mean_vector(cleaned).reshape(1, -1)
#     # BASE_URL = "https://cookpad.com"

#     def contains_all(row_tokens, input_tokens):
#         return all(token in row_tokens for token in input_tokens)

#     filtered = recipes[recipes['tokens'].apply(lambda x: contains_all(x, cleaned))]
#     if category_filter:
#         filtered = filtered[filtered['Category'].str.lower() == category_filter]

#     if filtered.empty:
#         return jsonify({"recommendations": [], "message": "Tidak ada resep yang sesuai."})

#     filtered_vectors = np.vstack(filtered['vector'].to_numpy())
#     sims = cosine_similarity(vector, filtered_vectors)[0]
#     top_indices = sims.argsort()[-10:][::-1]

#     result = filtered.iloc[top_indices][['Title', 'ingredients_clean', 'Category', 'Loves', 'URL']].copy()
#     result = result.rename(columns={"ingredients_clean": "Ingredients"})
#     # result['URL'] = BASE_URL + result['URL'].fillna("").astype(str)
#     result['URL'] = result['URL'].fillna("").astype(str)
#     result['score'] = sims[top_indices]

#     return jsonify({"recommendations": result.to_dict(orient="records")})
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    category_filter = data.get("category", "").strip().lower()

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    cleaned = clean_ingredients(" ".join(ingredients))
    vector = get_mean_vector(cleaned).reshape(1, -1)

    def contains_any(row_tokens, input_tokens):
        return any(token in row_tokens for token in input_tokens)

    filtered = recipes[recipes['tokens'].apply(lambda x: contains_any(x, cleaned))]

    if category_filter:
        filtered = filtered[filtered['Category'].str.lower() == category_filter]

    if filtered.empty:
        return jsonify({"recommendations": [], "message": "Tidak ada resep yang sesuai."})

    filtered_vectors = np.vstack(filtered['vector'].to_numpy())
    sims = cosine_similarity(vector, filtered_vectors)[0]
    top_indices = sims.argsort()[-10:][::-1]

    result = filtered.iloc[top_indices][['Title', 'ingredients_clean', 'Category', 'Loves', 'URL']].copy()
    result = result.rename(columns={"ingredients_clean": "Ingredients"})
    result['URL'] = result['URL'].fillna("").astype(str)
    result['score'] = sims[top_indices]

    return jsonify({"recommendations": result.to_dict(orient="records")})

@app.route("/categories")
def categories():
    unique = sorted(set(recipes['Category'].dropna().unique()))
    return jsonify({"categories": unique})

@app.route("/static/<filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
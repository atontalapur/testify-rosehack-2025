import logging
from flask import Flask, request, jsonify
from openai import OpenAI


import os

import zipfile
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


openai.api_key = os.getenv("OPENAI_API_KEY", "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")
# client=OpenAI(
#   api_key=""
# )
# Set OpenAI API key (replace with your key or set via environment variables)

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder and allowed file types
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'zip', 'pdf', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_pdf(content, output_path):
    """Generate a PDF file with the given content."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 50  # Start 50 units from the top
    
    for line in content.split("\n"):
        if y < 50:  # Move to next page if content overflows
            c.showPage()
            y = height - 50
        c.drawString(50, y, line)
        y -= 15  # Line spacing

    c.save()

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Server is working!"})


@app.route('/upload-and-process', methods=['POST'])
def upload_and_process():
    """
    Endpoint to upload a ZIP file, extract its contents, process them, and send a prompt to OpenAI.
    """
    test_endpoint()
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        prompt = request.form.get('prompt', '')

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only ZIP files are allowed."}), 400

        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract ZIP file contents
        extracted_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted')
        os.makedirs(extracted_folder, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        # Combine extracted text files into a single prompt
        combined_text = ""
        for root, dirs, files in os.walk(extracted_folder):
            for name in files:
                file_path = os.path.join(root, name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    combined_text += f.read() + "\n"

        # Send the combined text and prompt to OpenAI
        response = openai.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are analyzing the contents of a ZIP file."},
            {"role": "user", "content": f"{prompt}\n\nContents:\n{combined_text}"}
        ])

        print(response)

        # Simulated response files (adjust as needed)
        file_1_content = response.choices[0].message.content + "\nThis is File 1."
        file_2_content = response.choices[0].message.content + "\nThis is File 2."

        # Save response files
        output_file_1 = os.path.join(app.config['UPLOAD_FOLDER'], "output_file_1.pdf")
        output_file_2 = os.path.join(app.config['UPLOAD_FOLDER'], "output_file_2.pdf")

        generate_pdf(file_1_content, output_file_1)
        generate_pdf(file_2_content, output_file_2)

        # with open(output_file_1, "w") as f1:
        #     f1.write(file_1_content)

        # with open(output_file_2, "w") as f2:
        #     f2.write(file_2_content)

        # Return paths to the generated files
        return jsonify({
            "message": "File processed successfully.",
            "output_files": [output_file_1, output_file_2]
        })

    except Exception as e:
        logging.exception("Error processing file")
        return jsonify({"error": str(e)}), 500

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

app.run()

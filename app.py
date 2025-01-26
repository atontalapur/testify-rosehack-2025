from flask import Flask, send_file, jsonify
import os
from openai import OpenAI

client = OpenAI(api_key='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')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize OpenAI client

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    # Interact with GPT (customize the prompt as needed)
    prompt = f"Process the following text and generate output:\n\n{file_content}"
    try:
        response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model
        messages=[
                {"role": "system", "content": "You are analyzing the contents of a file."},
                {"role": "user", "content": prompt}
            ],
        max_tokens=1000)
        generated_text = response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating text: {str(e)}"

    # Save the generated output to a new file
    output_file_path = "output.txt"
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(generated_text)
    except Exception as e:
        return f"Error writing output file: {str(e)}"

    return output_file_path

@app.route('/process-file', methods=['GET'])
def process_file_route():
    file_path = '/Users/advaithtontalapur/Downloads'  # Specify the file path here
    output_file_path = process_file(file_path)
    if output_file_path.startswith("Error"):
        return jsonify({"error": output_file_path}), 500
    return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, port=3000)
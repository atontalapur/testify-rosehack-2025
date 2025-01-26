from flask import Flask, send_file, jsonify
import os
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize OpenAI client
openai.api_key = 'your_openai_api_key'

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    # Interact with GPT (customize the prompt as needed)
    prompt = f"Process the following text and generate output:\n\n{file_content}"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Use the appropriate model
            prompt=prompt,
            max_tokens=1000
        )
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
    file_path = 'C:/Users/danis/Downloads/Lab_1.pdf'  # Specify the file path here
    output_file_path = process_file(file_path)
    if output_file_path.startswith("Error"):
        return jsonify({"error": output_file_path}), 500
    return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, port=3000)
from flask import Flask, request, jsonify, send_file
import os
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize OpenAI client
openai_api_key = "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"
client = openai.OpenAI(api_key=openai_api_key)

# Create assistant and vector store
assistant = client.beta.assistants.create(
    name="Financial Analyst Assistant",
    instructions="You are an expert financial analyst. Use your knowledge base to answer questions about audited financial statements.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Financial Statements")

def process_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    # Upload the file to the vector store
    try:
        file_streams = [open(file_path, "rb")]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
        if file_batch.status != "completed":
            return f"Error uploading file: {file_batch.status}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"

    # Interact with GPT (customize the prompt as needed)
    prompt = f"Analyze the following financial document:\n\n{file_content.decode('utf-8', errors='ignore')}"
    try:
        response = client.chat_completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are analyzing the contents of a financial document."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        generated_text = response.choices[0].message['content'].strip()
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

@app.route('/process-file', methods=['POST'])
def process_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        output_file_path = process_file(file_path)
        if output_file_path.startswith("Error"):
            return jsonify({"error": output_file_path}), 500
        return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=3000)
from openai import OpenAI
import os
from flask import Flask, send_file, jsonify
import zipfile
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = api_key)

assistant = client.beta.assistants.create(
name="Questions creator",
instructions="Objective: Read and analyze all files provided using advanced content extraction tools like file parsing, text scanning, and data interpretation. The files may include various formats such as PDF, PPTX, Word documents, or plain text. Output Requirements: Based on the analyzed content: Generate a minimum of 10 diverse questions and their answers that align with the material. The questions should include: Factual questions (e.g., definitions, facts from the content). Analytical questions (e.g., explain or discuss topics). Application-based questions (e.g., apply concepts from the content). Critical thinking questions (e.g., evaluate or synthesize content ideas). Provide answers to each question with clear explanations. Tools: Utilize: File scanning and content extraction APIs. Contextual understanding and summarization technologies. Vector search for semantic alignment with the content. Formatting: Questions and answers should be numbered and presented in a clear, readable format. Ensure questions cover all key topics or sections of the files. Fallback: If certain files are not readable or extractable, use Python-based OCR or other parsing libraries to interpret the content and create meaningful questions. Output: Output ONLY the questions and nothing else.",
model="gpt-4o",
temperature=0.1,
tools=[{"type": "file_search"}],
)

# extracted_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted')
# os.makedirs(extracted_folder, exist_ok=True)
# with zipfile.ZipFile(r"/Users/advaithtontalapur/Documents/Advaith/rosehack-2025", 'r') as zip_ref:
#     zip_ref.extractall(extracted_folder)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Lecture Slides")

# Ready the files for upload to OpenAI
file_paths = [ r"/Users/advaithtontalapur/Documents/Advaith/rosehack-2025/uploads/extracted/Test/Jan6Econ003.pdf", r"/Users/advaithtontalapur/Documents/Advaith/rosehack-2025/uploads/extracted/Test/Jan8Econ003.pdf", r"/Users/advaithtontalapur/Documents/Advaith/rosehack-2025/uploads/extracted/Test/Jan10Econ003.pdf"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
vector_store_id=vector_store.id, files=file_streams
)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
assistant_id=assistant.id,
tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# Upload the user provided file to OpenAI
message_file = client.files.create(
file=open(r"/Users/advaithtontalapur/Downloads/Attendance.pdf", "rb"), purpose="assistants"
)

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
messages=[
  {
    "role": "user",
    "content": "It is a lecture slides shared with me by my professor. You have to use it to generate questions.",
    # Attach the new file to the message.
    "attachments": [
      { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
    ],
  }
]
)

# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI

client = OpenAI()

class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text) -> None:
      print(f"\nassistant > ", end="", flush=True)

  @override
  def on_tool_call_created(self, tool_call):
      print(f"\nassistant > {tool_call.type}\n", flush=True)

  @override
  def on_message_done(self, message) -> None:
      # print a citation to the file searched
      message_content = message.content[0].text
      annotations = message_content.annotations
      citations = []
      for index, annotation in enumerate(annotations):
          message_content.value = message_content.value.replace(
              annotation.text, f"[{index}]"
          )
          if file_citation := getattr(annotation, "file_citation", None):
              cited_file = client.files.retrieve(file_citation.file_id)
              citations.append(f"[{index}] {cited_file.filename}")

      
      generated_questions = message_content.value.strip()
      print(message_content.value)
      output_file_path = "output.pdf"
      pdf = FPDF()
      pdf.add_page()
      pdf.set_auto_page_break(auto=True, margin=15)
      pdf.set_font("Arial", size=12)
      pdf.multi_cell(0, 10, generated_questions)
      pdf.output(output_file_path)



# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="The user has a premium account.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()
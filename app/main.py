import os
from flask import Flask, request, render_template, send_from_directory
from PyPDF2 import PdfMerger

# Define the base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, '../templates'),
            static_folder=os.path.join(BASE_DIR, '../static'))

# Configure the upload folder relative to the base directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Get the uploaded files
    files = request.files.getlist('files')

    # Create a PdfMerger object
    merger = PdfMerger()

    # Add the uploaded files to the merger
    for file in files:
        merger.append(file)

    # Create the output file path
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged.pdf')

    # Write the merged PDF to the output file
    with open(output_path, 'wb') as f:
        merger.write(f)

    # Close the merger
    merger.close()

    # Send the merged file to the user for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'merged.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

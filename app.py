from flask import Flask, send_from_directory
import os

# Create Flask app
app = Flask(__name__)

# Get the directory of the current file
project_root = os.path.dirname(os.path.abspath(__file__))

# Configure the static folder
app = Flask(__name__, static_folder='static')

# Route to serve index.html
@app.route('/')
def serve_index():
    return send_from_directory(project_root, 'index.html')

# Route to serve images
@app.route('/image/<path:filename>')
def serve_images(filename):
    images_dir = os.path.join(project_root, 'image')
    return send_from_directory(images_dir, filename)

# Route to serve CSS files
@app.route('/css/<path:filename>')
def serve_css(filename):
    css_dir = os.path.join(project_root, 'css')
    return send_from_directory(css_dir, filename)

# This is for local development
if __name__ == '__main__':
    app.run(debug=True)
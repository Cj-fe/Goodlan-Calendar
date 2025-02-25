from flask import Flask, send_from_directory, request, jsonify
from activity_service import ActivityService
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

@app.route('/plugins/<path:filename>')
def serve_plugins(filename):
    plugins_dir = os.path.join(project_root, 'plugins')
    return send_from_directory(plugins_dir, filename)

@app.route('/insert-activity', methods=['POST'])
def insert_activity():
    try:
        data = request.json
        title = data.get('title')
        activity_date = data.get('activity_date')
        activity_end = data.get('activity_end')  # Added activity_end
        color_hex = data.get('color_hex')

        if not title or not activity_date or not activity_end or not color_hex:
            return jsonify({
                "success": False,
                "message": "Title, activity date, activity end date, and color hex are required"
            }), 400

        activity_service = ActivityService()
        result = activity_service.insert_activity(title, activity_date, activity_end, color_hex)

        if result["success"]:
            return jsonify({
                "success": True,
                "message": result["message"]
            })
        else:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/fetch-activities', methods=['GET'])
def fetch_activities():
    try:
        activity_service = ActivityService()
        result = activity_service.fetch_activities()

        if result["success"]:
            return jsonify({
                "success": True,
                "activities": result["activities"]
            })
        else:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/check-code', methods=['POST'])
def check_code():
    try:
        data = request.json
        code = data.get('code')

        if not code:
            return jsonify({
                "success": False,
                "message": "Code is required"
            }), 400

        activity_service = ActivityService()
        result = activity_service.check_code(code)

        if result["success"]:
            return jsonify({
                "success": True,
                "message": result["message"]
            })
        else:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

@app.route('/fetch-activity/<activity_id>', methods=['GET'])
def fetch_activity_by_id(activity_id):
    try:
        activity_service = ActivityService()
        result = activity_service.fetch_activity_by_id(activity_id)

        if result["success"]:
            return jsonify({
                "success": True,
                "activity": result["activity"]
            })
        else:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/update-activity', methods=['PUT'])
def update_activity():
    try:
        data = request.json
        activity_id = data.get('id')
        title = data.get('title')
        activity_date = data.get('activity_date')
        activity_end = data.get('activity_end')
        color_hex = data.get('color_hex')

        if not activity_id:
            return jsonify({
                "success": False,
                "message": "Activity ID is required"
            }), 400

        activity_service = ActivityService()
        result = activity_service.update_activity(activity_id, title, activity_date, activity_end, color_hex)

        if result["success"]:
            return jsonify({
                "success": True,
                "message": result["message"]
            })
        else:
            return jsonify({
                "success": False,
                "message": result["message"]
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# This is for local development
if __name__ == '__main__':
    app.run(debug=True)
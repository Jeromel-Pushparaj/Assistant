from flask import Flask, request, render_template_string
import webbrowser
import threading

app = Flask(__name__)

# HTML template with centered code display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrollable Text Container</title>
    <style>
        /* Reset margin and padding */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Full-screen container */
        body, html {
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }

        /* Centered, scrollable text container */
        .text-container {
            width: 80%;
            max-width: 600px;
            height: 70vh;
            padding: 20px;
            background-color: #fff;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            overflow-y: auto;
        }

        /* Styling for Markdown text */
        .text-container pre {
            font-size: 1rem;
            color: #333;
            white-space: pre-wrap; /* Ensures text wraps in pre */
            word-wrap: break-word; /* Breaks long words if needed */
            margin: 0;
        }
    </style>
</head>
<body>

    <div class="text-container">
        <pre>
        {{text}}
        </pre>
    </div>

</body>
</html>



"""

# Variable to store the posted text
display_text = ""

@app.route("/", methods=["GET"])
def display_text_page():
    return render_template_string(HTML_TEMPLATE, text=display_text or "No text received yet")

@app.route("/submit", methods=["POST"])
def receive_text():
    global display_text
    display_text = request.form.get("text", "")
    return "Text received successfully", 200

def run_server():
    app.run(debug=True, use_reloader=False)

# Start the server in a separate thread
threading.Thread(target=run_server).start()

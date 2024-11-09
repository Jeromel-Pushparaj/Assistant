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
    <title>Responsive Text Container</title>
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
            font-family: Arial, sans-serif;
        }

        /* Container with responsive text */
        .text-container {
            padding: 20px;
            width: 100%;
            max-width: 100vw;
            height: 100vh;
            overflow-wrap: break-word; /* Ensures long words break to fit */
        }

        /* Responsive text style */
        .text-container p {
            font-size: calc(10vw + 10vh); /* Adjusts based on viewport size */
            font-weight: bold;
            color: #333;
            margin: 0;
        }
    </style>
</head>
<body>

    <div class="text-container">
    <p>
        <pre>
        {{text}}
        </pre>
    </p>
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

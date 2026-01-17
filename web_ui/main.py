import os
import mistune
from flask import Flask, render_template
from markupsafe import Markup

app = Flask(__name__)

# The path to the operational log file inside the container
LOG_FILE_PATH = "/app/workspace/operational_log.md"

@app.route('/')
def index():
    """
    Reads the markdown log file, converts it to HTML, and renders it.
    """
    log_content_md = "## Operational Log Not Found\n\nPlease ensure the log file exists at `workspace/operational_log.md` and that the services have been started."
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r') as f:
            log_content_md = f.read()

    # Convert markdown to HTML
    log_content_html = Markup(mistune.html(log_content_md))

    return render_template('index.html', log_content=log_content_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

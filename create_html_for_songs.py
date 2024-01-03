# html_generator.py

def create_html_for_songs(song1, song2):
    return f"""
    <html>
    <head>
        <style>
            .video-container {{
                display: flex;
                justify-content: space-around;
                align-items: center;
            }}
            iframe {{
                margin: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="video-container">
            <div>
                <iframe width="560" height="315" src="https://www.youtube.com/embed/{song1['video_id']}" frameborder="0" allowfullscreen></iframe>
                <button onclick="choose(0)">選擇這首</button>
            </div>
            <div>
                <iframe width="560" height="315" src="https://www.youtube.com/embed/{song2['video_id']}" frameborder="0" allowfullscreen></iframe>
                <button onclick="choose(1)">選擇這首</button>
            </div>
        </div>
        <script>
            function choose(selection) {{
                window.pywebview.api.choose(selection);
            }}
        </script>
    </body>
    </html>
    """

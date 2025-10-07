from flask import Flask, render_template_string
import random

app = Flask(__name__)

html_template = """
<!doctype html>
<html>
<head>
  <title>🎨 Color Palette Picker</title>
  <style>
    /* Reset default margin/padding */
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body, html {
      height: 100%;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      overflow-x: hidden;
    }

    header {
      width: 100%;
      padding: 30px 0;
      background: linear-gradient(90deg, #ff7e5f, #feb47b);
      color: white;
      text-align: center;
      font-size: 2rem;
      font-weight: bold;
      box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .palette {
      display: flex;
      flex-direction: column;
      height: calc(100% - 90px); /* header height + some margin */
    }

    .color-strip {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .color-strip:hover {
      transform: scale(1.02);
      box-shadow: 0 8px 15px rgba(0,0,0,0.3);
    }

    .generate-btn {
      position: fixed;
      bottom: 30px;
      left: 50%;
      transform: translateX(-50%);
      padding: 15px 30px;
      font-size: 1.2rem;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 30px;
      cursor: pointer;
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
      transition: background 0.2s, transform 0.2s;
    }

    .generate-btn:hover {
      background: #45a049;
      transform: translateX(-50%) scale(1.05);
    }
  </style>
  <script>
    function copyColor(color) {
      navigator.clipboard.writeText(color).then(() => {
        alert(color + " copied to clipboard!");
      });
    }
  </script>
</head>
<body>
  <header>🎨 Random Color Palette Picker</header>

  <div class="palette">
    {% for color in colors %}
    <div class="color-strip" style="background-color: {{color}}" onclick="copyColor('{{color}}')">
      {{color}}
    </div>
    {% endfor %}
  </div>

  <form method="get">
    <button class="generate-btn">Generate New Palette</button>
  </form>
</body>
</html>
"""

def random_color():
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))

@app.route("/")
def home():
    colors = [random_color() for _ in range(5)]
    return render_template_string(html_template, colors=colors)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, Response
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

x_data, y_data = [], []

@app.route('/plot.png')
def plot_png():
    x_data.append(len(x_data))
    y_data.append(random.randint(0, 10))

    fig, ax = plt.subplots()
    ax.plot(x_data, y_data, color='blue')
    ax.set_title("Real-time Plot")
    ax.set_xlabel("Time step")
    ax.set_ylabel("Value")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Real-time Plot</h1>
            <img id="plot" src="/plot.png" width="600">
            <script>
                setInterval(function() {
                    document.getElementById('plot').src = '/plot.png?rand=' + Math.random();
                }, 1000);
            </script>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(port=5050, debug=False)

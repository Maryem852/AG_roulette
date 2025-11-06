from flask import Flask, render_template, request, jsonify
import random, math
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# --- Exemple de matrice pour TSP ---
matrice = [
    [0,2,2,7,15,2,5,7,6,5],
    [2,0,10,4,7,3,7,15,8,2],
    [2,10,0,1,4,3,3,4,2,3],
    [7,4,1,0,2,15,7,7,5,4],
    [15,7,4,2,0,7,3,2,2,7],
    [2,3,3,15,7,0,1,7,2,10],
    [5,7,3,7,3,1,0,1,2,7],
    [7,15,4,7,2,7,1,0,1,2],
    [6,8,2,5,2,2,2,1,0,15],
    [5,2,3,4,7,10,7,2,15,0]
]

def calculer_distance_totale(solution, matrice):
    d = 0
    for i in range(len(solution) - 1):
        d += matrice[solution[i]][solution[i + 1]]
    d += matrice[solution[-1]][solution[0]]
    return d


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['POST'])
def run_algorithm():
    algo = request.form['algo']
    croisement = request.form.get('croisement', None)

    # --- Pour la démo on simule un résultat ---
    villes = list(range(10))
    random.shuffle(villes)
    distance = calculer_distance_totale(villes, matrice)

    # --- Génération de la figure ---
    x = [random.random() * 10 for _ in villes]
    y = [random.random() * 10 for _ in villes]
    plt.figure(figsize=(5,5))
    plt.plot(x + [x[0]], y + [y[0]], '-o', color='#00eaff')
    for i, txt in enumerate(villes):
        plt.text(x[i]+0.1, y[i]+0.1, str(txt), fontsize=9, color='white')
    plt.title(f"Résultat {algo} - {croisement if croisement else ''}", color='white')
    plt.gca().set_facecolor('#0e1621')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    plt.close()
    return jsonify({'img': image_base64, 'distance': distance})


if __name__ == '__main__':
    app.run(debug=True)

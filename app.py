from flask import Flask, jsonify, request, render_template
import random
import math

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class KMeans:
    def __init__(self):
        self.reset()

    def reset(self):
        self.points = []
        self.centroids = []
        self.clusters = []
        self.k = 0

    def generate_points(self, num_points=50, x_range=(0, 100), y_range=(0, 100)):
        self.points = [[random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])] for _ in range(num_points)]
        return self.points

    def initialize_centroids(self, method='random', k=3, initial_centroids=[]):
        self.k = k
        if method == 'random':
            self.centroids = random.sample(self.points, k)
        elif method == 'farthest':
            self.centroids = [random.choice(self.points)]
            while len(self.centroids) < k:
                farthest = max(self.points, key=lambda p: min(self.euclidean(p, c) for c in self.centroids))
                self.centroids.append(farthest)
        elif method == 'kmeans++':
            self.centroids = [random.choice(self.points)]
            for _ in range(1, k):
                distances = [min(self.euclidean(p, c) for c in self.centroids) for p in self.points]
                total = sum(distances)
                probabilities = [d / total for d in distances]
                self.centroids.append(random.choices(self.points, weights=probabilities)[0])
        elif method == 'manual':
            self.centroids = initial_centroids
        self.clusters = [[] for _ in range(k)]

    def step(self):
        self.clusters = [[] for _ in range(self.k)]
        for point in self.points:
            closest_centroid = min(self.centroids, key=lambda centroid: self.euclidean(point, centroid))
            self.clusters[self.centroids.index(closest_centroid)].append(point)
        self.centroids = [self.recompute_centroid(cluster) for cluster in self.clusters]

    def euclidean(self, point1, point2):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

    def recompute_centroid(self, cluster):
        return [sum(coords) / len(cluster) for coords in zip(*cluster)] if cluster else random.choice(self.points)

kmeans = KMeans()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_data', methods=['POST'])
def generate_data():
    points = kmeans.generate_points()
    return jsonify(points)

@app.route('/initialize_kmeans', methods=['POST'])
def initialize_kmeans():
    data = request.json['data']
    kmeans.points = data
    kmeans.initialize_centroids(request.json['initialization'], request.json['k'], request.json.get('initial_centroids', []))
    return jsonify({'centroids': kmeans.centroids, 'clusters': kmeans.clusters})

@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    kmeans.step()
    return jsonify({'centroids': kmeans.centroids, 'clusters': kmeans.clusters})

@app.route('/run_kmeans_final', methods=['POST'])
def run_kmeans_final():
    for _ in range(100):
        previous_centroids = kmeans.centroids[:]
        kmeans.step()
        if kmeans.centroids == previous_centroids:
            break
    return jsonify({'centroids': kmeans.centroids, 'clusters': kmeans.clusters})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
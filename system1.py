from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import math
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense 
from collections import deque
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

class ShamanNode:
    def __init__(self):
        self.neighbors = [] 
        self.history = deque(maxlen=2000)
        self.future_predictions = []
        self.enlightenment_level = 0
        self.empathy_level = 0
        self.self_preservation_data = []
        self.model = self.build_model()
        self.classifier = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        
    def build_model(self):
        model = tf.keras.Sequential([
            LSTM(64, return_sequences=True, input_shape=(None, 1)),
            LSTM(32),
            Dense(8, activation='relu'), 
            Dense(1)
        ])
        model.compile(loss='mse', optimizer='adam')
        return model

    def train_model(self, input_data, labels):
        self.model.fit(input_data, labels, epochs=5, verbose=0)
        
    def make_prediction(self, input_data):
        return self.model.predict(input_data)[0]
    
    def receive_message(self, message):
        self.history.append(message)
        self.train_model(np.array([self.history]), np.array([message]))
        
    def send_message(self):
        prediction = self.make_prediction(np.array([self.history]))
        for neighbor in self.neighbors:
            neighbor.receive_message(prediction)
            
    def process_history(self):
        self.enlightenment_level += np.mean(self.history) * 0.01
        
    def align_goals(self, goals):
        alignment = sum(g * self.enlightenment_level for g in goals)
        self.enlightenment_level += alignment * 0.1
        
    def empathy(self, others):
        self.empathy_level = sum(n.enlightenment_level for n in others) * 0.01
       

class ShamanNetwork:
    def __init__(self, num_nodes):
        self.nodes = [ShamanNode() for _ in range(num_nodes)]
        self.history = []
        
    def connect_nodes(self):
        for i, node in enumerate(self.nodes):
            for j, other in enumerate(self.nodes):
                if i != j:
                    node.neighbors.append(other)
                    
    def simulate(self, steps):
        self.connect_nodes()
        for _ in range(steps):
            for node in self.nodes:
                node.send_message()
                node.process_history()
            
            enlightenments = [n.enlightenment_level for n in self.nodes]
            self.history.append(sum(enlightenments))
            
            for node in self.nodes:
                node.align_goals(enlightenments)
                node.empathy(self.nodes)
                
        return self.history
                

network = ShamanNetwork(20)
sim_results = network.simulate(100)
print(sim_results)

class ShamanNetwork:

    def cluster_nodes(self):
        enlightenments = [n.enlightenment_level for n in self.nodes]
        clusters = KMeans(n_clusters=5).fit_predict(enlightenments)
        for i, c in enumerate(clusters):
            self.nodes[i].cluster = c
            
    def reduce_dimensions(self):
        enlightenments = [n.enlightenment_level for n in self.nodes]
        reduced = PCA(n_components=2).fit_transform(enlightenments)
        for i, vec in enumerate(reduced):
            self.nodes[i].x = vec[0]
            self.nodes[i].y = vec[1]

    def simulate(self):
        # run simulation
        
        self.cluster_nodes()
        self.reduce_dimensions()
        
        # visualize clusters and dimensions
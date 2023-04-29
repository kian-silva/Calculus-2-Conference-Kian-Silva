#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
from numpy import random
from geopy import distance
import plotly.graph_objects as go


circuit_list = [{"lon": 50.512, "lat": 26.031, "location": "Sakhir", "name": "Bahrain International Circuit"},
                {"lon": 39.104, "lat": 21.632, "location": "Jeddah", "name": "Jeddah Corniche Circuit"},
                {"lon": 144.970, "lat": -37.846, "location": "Melbourne", "name": "Albert Park Circuit"},
                {"lon": 49.842, "lat": 40.369, "location": "Baku", "name": "Baku City Circuit"},
                {"lon": -80.239, "lat": 25.958, "location": "Miami", "name": "Miami International Autodrome"},
                {"lon": 11.713, "lat": 44.341, "location": "Imola", "name": "Autodromo Enzo e Dino Ferrari"},
                {"lon": 7.429, "lat": 43.737, "location": "Monte Carlo", "name": "Circuit de Monaco"},
                {"lon": 2.259, "lat": 41.569, "location": "Barcelona", "name": "Circuit de Barcelona-Catalunya"},
                {"lon": -73.525, "lat": 45.506, "location": "Montreal", "name": "Circuit Gilles-Villeneuve"},
                {"lon": 14.761, "lat": 47.223, "location": "Spielberg", "name": "Red Bull Ring"},
                {"lon": -1.017, "lat": 52.072, "location": "Silverstone", "name": "Silverstone Circuit"},
                {"lon": 19.250, "lat": 47.583, "location": "Budapest", "name": "Hungaroring"},
                {"lon": 5.971, "lat": 50.436, "location": "Spa Francorchamps", "name": "Circuit de Spa-Francorchamps"},
                {"lon": 4.541, "lat": 52.389, "location": "Zandvoort", "name": "Circuit Zandvoort"},
                {"lon": 103.859, "lat": 1.291, "location": "Singapore", "name": "Marina Bay Street Circuit"},
                {"lon": 136.534, "lat": 34.844, "location": "Suzuka", "name": "Suzuka International Racing Course"},
                {"lon": 51.454, "lat": 25.49, "location": "Lusail", "name": "Losail International Circuit"},
                {"lon": -97.633, "lat": 30.135, "location": "Austin", "name": "Circuit of the Americas"},
                {"lon": -99.091, "lat": 19.402, "location": "Mexico City", "name": "Autódromo Hermanos Rodríguez"},
                {"lon": -46.698, "lat": -23.702, "location": "Sao Paulo", "name": "Autódromo José Carlos Pace - Interlagos"},
                {"lon": -115.168, "lat": 36.116, "location": "Las Vegas", "name": "Las Vegas Street Circuit"},
                {"lon": 54.601, "lat": 24.471, "location": "Abu Dhabi", "name": "Yas Marina Circuit"}
               ]

    
        
# compute total distance of travelled between circuits using the current calendar route
def total_distance(circuit_list):
    d = 0.0 # in Km
    n = len(circuit_list)
    nxt = 0
    for i in range(n):
        if i == n -1:
            b = 0
        else:
            b = i + 1
        cordsA = (circuit_list[i]["lat"], circuit_list[i]["lon"])
        cordsB = (circuit_list[b]["lat"], circuit_list[b]["lon"])
        if cordsA < cordsB:
            diff =  distance.distance(cordsA, cordsB).km *1.0
            d += diff
            circuit_list[i]["distance"] = round(diff,3)
        else:
            diff = distance.distance(cordsB, cordsA).km *1.5
            d += diff
            circuit_list[i]["distance"] = round(diff,3)    
    return round(d,3)

#calculate an error to find the most optimal distance 
def error(circuit_list):
    n = len(circuit_list)
    d = total_distance(circuit_list)
    min_dist = n - 1
    return d - min_dist

#swaps two random indices from the first route making a new route
def swap(circuit_list):
    n = len(circuit_list)
    shuffle = np.copy(circuit_list)
    i, j = np.random.randint(n), np.random.randint(n)
    hold = shuffle[i]
    shuffle[i],shuffle[j] = shuffle[j], hold
    return shuffle

def printVal(value, circ):
    val = []
    for i in range(len(circ)):
        val.append(circ[i][value])
    return ", ".join(val)
        
def solve(circuit_list, max_iter, start_temp, alpha, rnd):
    curr_temp = start_temp
    circ = circuit_list
    err = error(circ)
    iteration = 0
    interval = (int)(max_iter / 10)
    

    while iteration < max_iter and err > 0.0:
        adj_circ = swap(circ)
        adj_err = error(adj_circ)
    
        if adj_err < err:
            circ, err = adj_circ, adj_err
        else:
            accept_p = np.exp((err-adj_err) / curr_temp)
            p = rnd.random()
            if p < accept_p:
                circ, err = adj_circ, adj_err
    
        if iteration % interval == 0:
            print("iter = %6d | curr error = %7.2f | temperature = %10.4f " % (iteration, err, curr_temp))
    
        if curr_temp < 0.0001:
            curr_temp = 0.0001
        else:
            curr_temp = curr_temp * alpha
        iteration += 1    
    return circ

def mapCirc(circ):
    lonC = []
    latC = []
    locC = []
    
    for i in range(len(circ)):
        lonC.append(circ[i]["lon"])
        latC.append(circ[i]["lat"])
        locC.append(circ[i]["location"])
        
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = lonC,
        lat = latC,
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "open-street-map",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1 })
    fig.update_traces(
        text = locC)
    fig.show()
    
def main():
    mapCirc(circuit_list)
    print("Current F1 calendar map")
    circuit_dist = total_distance(circuit_list)
    print("Current total distance of F1 Calendar Map = %0.1f" % circuit_dist)
    rnd = np.random.RandomState(4) 
    max_iter = 2500
    start_temperature = 10000.0
    alpha = 0.99
    print("max_iter = %d " % max_iter)
    print("start_temperature = %0.1f " % start_temperature)
    print("alpha = %0.2f " % alpha) 
    best = solve(circuit_list, max_iter, start_temperature, alpha,rnd)
    print("\nBest solution found: ")
    bestLoc = printVal('location', best)
    print(bestLoc)
    dist = total_distance(best)
    print("\nTotal distance = %0.1f " % dist)
    mapCirc(best)
    

if __name__ == "__main__":
    main()

            


# In[ ]:





# In[ ]:





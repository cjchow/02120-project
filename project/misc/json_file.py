import json
import numpy as np

d = {"name": "soot only", "tau_soot": 8.0, "temps": np.array([288.0, 285.2, 279.9]).tolist()}

# opens a file for Writing (creates it if it didn't previously exist). The file closes 
with open("test.json", "w") as f:
    # takes the dictionary d and writes it in to file f as JSON text
    json.dump(d, f)
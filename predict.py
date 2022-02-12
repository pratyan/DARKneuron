import pickle
import numpy as np
from model import create_disease_hash,get_symp_hash

disease_hash = create_disease_hash()
symp_hash = get_symp_hash()


def load_model(path):
	with open(path, 'rb') as file:
		pickle_model = pickle.load(file)
	return pickle_model
   
def predict(model,data):
	d = np.zeros(shape=(1,len(symp_hash)))

	for i in range(len(data)):
		d[0][symp_hash[data[i]]] = 1		
	print(m.predict(d))	
		
l = ['itching','skin_rash',]
m = load_model('rf.pkl')

predict(m,l)
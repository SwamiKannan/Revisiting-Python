import pickle


with open('activity+month+year.pkl', 'rb') as handle:
    b = pickle.load(handle)


print(b)
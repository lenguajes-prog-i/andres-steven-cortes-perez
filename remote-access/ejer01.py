import pickle 

data = {"mensaje" : "Hola"}

serializacion = pickle.dumps(data)

#print(serializacion)

mensaje = pickle.loads(serializacion)

print(mensaje)



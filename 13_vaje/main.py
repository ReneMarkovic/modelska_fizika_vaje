import silicon_mind as sm

#Parametri za inicializacijo nevronske mreže
#arhitektura=[]
brain=sm.ustvari_nevronsko_mrezo([1,3,1],"tanh")
print(sm.activation_function(3,"sigmoid",False)) #Izracuna f(x)
print(sm.activation_function(3,"sigmoid",True)) #Izracuna f'(x)
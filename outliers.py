import numpy
# quicksort for ordering stuff
def quicksort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return quicksort(less)+equal+quicksort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

def calcularPromedio(aux):
    promedio = 0
    size = len(aux)
    for x in aux:
        promedio =+ x
    promedio = promedio/size
    return promedio

def calcularT(x):
    y = {
        3: 1.1511,
        4: 1.4250,
        5: 1.5712,
        6: 1.6563,
        7: 1.7110,
        8: 1.7491,
        9: 1.7770,
        10: 1.7984,
        11: 1.8153,
        12: 1.8290,
        13: 1.8403,
        14: 1.8498,
        15: 1.8579,
        16: 1.8649,
        17: 1.8710,
        18: 1.8764,
        19: 1.8811,
        20: 1.8853,
        21: 1.8891,
        22: 1.8926,
        23: 1.8957,
        24: 1.8985,
        25: 1.9011,
        26: 1.9035,
        27: 1.9057,
        28: 1.9078,
        29: 1.9096,
        30: 1.9114,
        31: 1.9130,
        32: 1.9146,
        33: 1.9160,
        34: 1.9174,
        35: 1.9186,
        36: 1.9198,
        37: 1.9209,
        38: 1.9220,
    }
    try:
        return y[x]
    except:
        if (39 <= x <= 50):
            return 1.9314
        if (51 <= x <= 100):
            return 1.9459
        if (101 <= x <= 1000):
            return 1.9586
    return 1.9600

def removeOutliersAux(aux):
    print "estoy en la func"
    size = len(aux)
    #desvios = []
    promedio = calcularPromedio(aux)
    desvio = numpy.std(aux)
    print desvio
    #for x in aux:
    #    desvios.append(abs(x-promedio))
    #print size
    t = calcularT(size)
    #print t
    #print desvios
    desvio_1 = abs(aux[0] - promedio)
    desvio_n = abs(aux[size-1] - promedio)

    maximo = max(desvio_1, desvio_n)
    if(maximo == desvio_1):
        if(t*desvio > maximo):
            aux2 = aux.pop(0)
            return removeOutliersAux(aux2)
    if(maximo == desvio_n):
        print "tengo que entrar aca"
        print t*desvio
        if(t*desvio > maximo):
            aux3 = aux.pop(size-1)
            return removeOutliersAux(aux3)
    return aux


# we define the function to calculate outliers
# - def removeOutliers(measure):

array = [13, 14, 15, 12, 16, 13, 12, 300000, 14, 13, 14]
aux = quicksort(array)
result = removeOutliersAux(aux)
print result

# - return removeOutliersAux(aux)

#Aca empieza el codigo:
#me pasan easure
#ordenamos con quicksort
#loopeamos
 #size = tam meas
 #creamos desvios_i

 #calculo el desvio standard del primer y ultimo valor, y los multiplico por la cosa esa que no recuerdo de donde sale



 #calculamos desvio_stand_para cada i en easure y lo asignamos a desvios_i
 #seteamos t con el value de t en la tabla
 #checkeamos d1 y dn vs t.
 #si alguno es outlier, lo sacamos de measure y loopeamos.
 #si no, termino.

# printing result
#print(result)
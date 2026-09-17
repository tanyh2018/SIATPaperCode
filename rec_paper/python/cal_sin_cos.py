import math

def cos_sum(k, M):
    s = 0
    for i in range(1, k+1):
        s += math.cos(2*i*math.pi/M)
    return s

def cos2_sum(k, M):
    s = 0
    for i in range(1, k+1):
        s += (math.cos(2*i*math.pi/M))**2
    return s


def sim_sum(k, M):
    s = 0
    for i in range(1, k+1):
        s += math.sin(2*i*math.pi/M)
    return s

def main():
     A = cos_sum(5,5)
     B = sim_sum(10,10)
     print(A,B)
if __name__ == '__main__':
      main()
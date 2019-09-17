def formula(base, n, startx):
    nextx = (1/n)*((n-1)*startx+base/startx**(n-1))
    return(nextx)


def iterate(base, n):
    startx = base / 2
    result = formula(base, n, startx)
    i = 0
    while True:
        result_n = formula(base, n, result)
        delta = (result_n - result)
        #print(i, ">>>", result, result_n, delta)
        if abs(delta) < 0.00000000000000000000000001:
            return result_n
        else:
            result = result_n
            i+=1

def find_limit(base, n):
    start_base = base
    start_n = n
    conditions = {"base": "n"}
    while True:
        try:
            try:
                res = iterate(base, n)
                #print(n, base, " >>> ", res)
                base = base*2
            except:
                conditions[base/2] = n
                print("limit:    ", n, base, " >>> ", iterate(base/2, n))
                n+=1
                base=start_base
                iterate(base, n)
        except:
            return conditions







if __name__ == '__main__':

    print(find_limit(99999999999, 2))
    #print(iterate(999999999999, 2))


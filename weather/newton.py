#!/usr/bin/python3
import json
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup as Bs
from cities_dict import get_cities
from datetime import datetime, date, time, timedelta
from multiprocessing.dummy import Pool as ThPool
import subprocess
import multiprocessing as mp
from subprocess import check_output

def formula_newton(base, exp, startx):
    nextx = (1/exp)*((exp-1)*startx+base/startx**(exp-1))
    return(nextx)


def iterate_newton(base, exp, startx):

    #try:
        #startx = int(base / div)
    #except:
        #startx = base / div
    
    #startx = base / div
        #print(type(startx))
    #print(base, exp, startx)
    result = formula_newton(base, exp, startx)
    delta = 0
    i = 0
    while True:
        #print(base, exp, result)
        result_n = formula_newton(base, exp, result)
        delta_n = (result_n - result)
        #print(i, div, ">>>", result, result_n, delta)
        if abs(delta_n) < 0.000000000000000000000000001:
            return result_n
        else:
            if abs(delta) == abs(delta_n):
                #print(i, div, ">>>", result, result_n, delta)
                return("no result")
            result = result_n
            delta = delta_n
            i+=1

            
def vary_startx(base, exp):
    for i in [1+10**-6, 1+10**-5, 1+10**-4, 1+10**-3, 1+10**-2, 2,3,5,10,50,10**3, 10**3, 10**4, 10**5, 10**10, 10**20, 10**50]:
        try:
            res = iterate_newton(base, exp, i)
            if res == iterate_newton(base, exp, i) != "no result":
                return res
        except:
            pass        

def find_limit_newton(base, exp):
    try:
        res = vary_startx(base, exp)
        #print(exp, base, " >>> ", res)
        while True:
            base_prev = base
            base = base*10
            #print("exp ", exp, len(str(base)), " >>> ", res)
            res == vary_startx(base, exp)
            if vary_startx(base, exp) != None:
                pass
                #print(vary_startx(base, exp))
            else:
                print("exp {}, base 1e +{} >>> no result".format(exp, len(str(base))))
                res = vary_startx(base_prev, exp)
                print("limit: 1e +", len(str(base))-1)
                print("result: ", res)
                return res
    except:
        #print("base {}, exp {} >>> no result".format(base, exp))
        print(base)
        base = base/10
        while True:
            try:
                res = vary_startx(base, exp)
                print("exp {}, base 1e +{} >>> no result".format(exp, len(str(base*2))))
                l = len(str(base))         
                print("limit: {}".format(l))
                print("result: ", len(str(res)))
                return res
            except:
                #print("base {}, exp {} >>> no result".format(base, exp))
                base = base/2
                
def vary_exp():
    for i in [2,3,4,5,6,7,8,9,10,20,30,40,50,100,500,10**3,10**4, 10**5, 10**6]:
        find_limit_newton(10**50, i)
        



if __name__ == '__main__':


    vary_exp()
    
    #print(1000**(1/10000))
    #print(formula_newton(1000, 10000, 2))
    #print(iterate_newton(10**308, 2, 1+10**-6))
    #print(vary_startx(10**309,2))
    

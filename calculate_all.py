# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:27:14 2018

@author: Francesco
"""

from pomegranate import *
from smarthouse import *
import numpy as np
import matplotlib.pyplot as plt
def ourModel(n,tipo):
   
    act_names = ['Breakfast','Dinner','Grooming','Leaving','Lunch','Showering',
                 'Sleeping','Snack','Spare_Time/TV','Toileting']
    if tipo== "A":    
        #Emissioni Ordonez_A
        obs_names = ['Basin', 'Bed', 'Cabinet', 'Cooktop', 'Cupboard', 'Fridge',
                     'Maindoor', 'Microwave', 'Seat', 'Shower', 'Toaster', 'Toilet']
    else:
        #Emissioni Ordonez_B
        obs_names = ['Basin','Bed','Cupboard','Door Bathroom','Door Bedroom',
                     'Door Kitchen','Fridge','Maindoor','Microwave','Seat','Shower',
                     'Toilet']
    
    if tipo =="A":
        path = './OrdonezA_integrated.txt'
    else:
        
        path = './OrdonezB_integrated.txt'
    

    act_gt,obs_gt = setup(path)
    ysc2=[]
    ydif2=[]
    
    
    #One-Day Validation
    
    training_obs = obs_gt[:n]
    training_act = act_gt[:n]
    test_obs = obs_gt[n:]
    test_act = act_gt[n:]
  
    init_distr = init_prob(flatten(training_act), act_names)
    trans_distr = trans_prob(flatten(training_act), act_names)
    ems_distr = ems_prob(flatten(training_act),flatten(training_obs), act_names, obs_names)
    
    d = [dict(zip(obs_names,ems_distr[i])) for i in range(len(ems_distr))]
    dists = [DiscreteDistribution(x) for x in d]
    model = HiddenMarkovModel.from_matrix(trans_distr, dists, init_distr, state_names = act_names, verbose=True)
    seq = [state.name for i, state in model.viterbi(flatten(test_obs))[1]][1:]
    ysc=score(seq,flatten(test_act),act_names)
    ydif=seq_diff(seq,flatten(test_act))
    ysc2.append(ysc)
    ydif2.append(ydif)
        
      
   
    string1= "Differenza nostro modello \n" + str(ydif2)+"\n"+ "F-measure nostro modello\n"+str(ysc2)+"\n"
    return string1


def baseline(n,tipo):
        #Attività
    act_names = ['Breakfast','Dinner','Grooming','Leaving','Lunch','Showering',
                 'Sleeping','Snack','Spare_Time/TV','Toileting']
    
    if tipo== "A":    
        #Emissioni Ordonez_A
        obs_names = ['Basin', 'Bed', 'Cabinet', 'Cooktop', 'Cupboard', 'Fridge',
                     'Maindoor', 'Microwave', 'Seat', 'Shower', 'Toaster', 'Toilet']
    else:
        #Emissioni Ordonez_B
        obs_names = ['Basin','Bed','Cupboard','Door Bathroom','Door Bedroom',
                     'Door Kitchen','Fridge','Maindoor','Microwave','Seat','Shower',
                     'Toilet']
    
    #parametri del modello equiprobabile (Baseline)
    init_distr = [1/len(act_names) for i in range(len(act_names))]
    trans_distr = [[1/len(act_names) for i in range(len(act_names))] for i in range(len(act_names))]
    ems_distr = dict(zip(obs_names, [1/len(obs_names) for i in range(len(obs_names))]))
    
    dists = [DiscreteDistribution(ems_distr) for i in range(len(act_names))]
    model = HiddenMarkovModel.from_matrix(trans_distr, dists, init_distr, state_names = act_names, verbose=True)
    
    if tipo =="A":
        path = './OrdonezA_integrated.txt'
    else:
        path = './OrdonezB_integrated.txt'    
        
    act_gt, obs_gt = setup(path)
        
    ysc2=[]
    ydif2=[]
    
    #One-Day Validation
    
    training_obs = obs_gt[:n]
    training_act = act_gt[:n]
    test_obs = obs_gt[n+1:]
    test_act = act_gt[n+1:]
    
    model.fit(training_obs, algorithm = 'labeled', labels = training_act)
    seq = [state.name for i, state in model.viterbi(flatten(test_obs))[1]][1:]
    ysc=score(seq,flatten(test_act),act_names)
    ydif=seq_diff(seq,flatten(test_act))
    ysc2.append(ysc)
    ydif2.append(ydif)
     

    string1= "Differenza modello equiprobabile con addestramento\n" + str(ydif2)+"\n"+"F-measure modello equiprobabile con addestramento\n"+str(ysc2)+"\n"
    return string1
def equiprob(n,tipo):
        #Attività
    act_names = ['Breakfast','Dinner','Grooming','Leaving','Lunch','Showering',
                 'Sleeping','Snack','Spare_Time/TV','Toileting']
    
    if tipo== "A":    
        #Emissioni Ordonez_A
        obs_names = ['Basin', 'Bed', 'Cabinet', 'Cooktop', 'Cupboard', 'Fridge',
                     'Maindoor', 'Microwave', 'Seat', 'Shower', 'Toaster', 'Toilet']
    else:
        #Emissioni Ordonez_B
        obs_names = ['Basin','Bed','Cupboard','Door Bathroom','Door Bedroom',
                     'Door Kitchen','Fridge','Maindoor','Microwave','Seat','Shower',
                     'Toilet']
    #parametri del modello equiprobabile (Baseline)
    init_distr = [1/len(act_names) for i in range(len(act_names))]
    trans_distr = [[1/len(act_names) for i in range(len(act_names))] for i in range(len(act_names))]
    ems_distr = dict(zip(obs_names, [1/len(obs_names) for i in range(len(obs_names))]))
    
    dists = [DiscreteDistribution(ems_distr) for i in range(len(act_names))]
    model = HiddenMarkovModel.from_matrix(trans_distr, dists, init_distr, state_names = act_names, verbose=True)
    
    if tipo =="A":
        path = './OrdonezA_integrated.txt'
    else:
        path = './OrdonezB_integrated.txt'
        
    act_gt, obs_gt = setup(path)
    ysc2=[]
    ydif2=[]
    
    #One-Day Validation
   
    test_obs = obs_gt[n+1:]
    test_act = act_gt[n+1:]
    
    seq = [state.name for i, state in model.viterbi(flatten(test_obs))[1]][1:]
    ysc=score(seq,flatten(test_act),act_names)
    ydif=seq_diff(seq,flatten(test_act))
    ysc2.append(ysc)
    ydif2.append(ydif)
     

    string2= "Differenza modello equiprobabile\n" + str(ydif2)+"\n"+ "F-measure modello equiprobabile \n"+str(ysc2)+"\n"
    return string2
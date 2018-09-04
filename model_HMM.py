from pomegranate import *
from smarthouse import *
import numpy as np
import matplotlib.pyplot as plt

act_names = ['Breakfast','Dinner','Grooming','Leaving','Lunch','Showering',
             'Sleeping','Snack','Spare_Time/TV','Toileting']

#Emissioni Ordonez_A
#obs_names = ['Basin', 'Bed', 'Cabinet', 'Cooktop', 'Cupboard', 'Fridge',
#             'Maindoor', 'Microwave', 'Seat', 'Shower', 'Toaster', 'Toilet']

#Emissioni Ordonez_B
obs_names = ['Basin','Bed','Cupboard','Door Bathroom','Door Bedroom',
             'Door Kitchen','Fridge','Maindoor','Microwave','Seat','Shower',
             'Toilet']

path = './OrdonezB_integrated.txt'
act_gt,obs_gt = setup(path)

diff_list = []
score_list = []

#One-Day Validation
for day in range(len(obs_gt)):
    test_obs = obs_gt[day]
    test_act = act_gt[day]
    training_obs = obs_gt[:day]+obs_gt[day + 1:]
    training_act = act_gt[:day]+act_gt[day + 1:]
    
    #Parametri del modello calcolati direttamente dalle istanze di training.
    init_distr = init_prob(flatten(training_act), act_names)
    trans_distr = trans_prob(flatten(training_act), act_names)
    ems_distr = ems_prob(flatten(training_act),flatten(training_obs), act_names, obs_names)
    
    d = [dict(zip(obs_names,ems_distr[i])) for i in range(len(ems_distr))]
    dists = [DiscreteDistribution(x) for x in d]
    model = HiddenMarkovModel.from_matrix(trans_distr, dists, init_distr, state_names = act_names, verbose=True)
    seq = [state.name for i, state in model.viterbi(test_obs)[1]][1:]
    error = seq_diff(seq,test_act)
    f_measure = score(seq,test_act,act_names)
    diff_list.append(error)
    score_list.append(f_measure)

x = np.arange(1,len(act_gt)+1)
plt.figure(num=None, figsize=(17, 10), dpi=72, facecolor='w', edgecolor='k')
ax = plt.subplot(111)
plt.ylabel('Differenza  ;  F-Measure')
plt.xlabel('Test Day')
plt.xticks(x)
sc = ax.bar(x+0.2,score_list,width=0.2,color='c',align='center')
dif = ax.bar(x-0.2,diff_list,width=0.2,color='g',align='center')
ax.autoscale(tight=True)

ax.legend((sc[0],dif[0]),('F-Measure','Differenza'))

plt.show()
    
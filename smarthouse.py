import re

#Setup delle variabili necessarie alla creazione dei modelli e all'utilizzo
#delle altre funzioni.Le variabili in output contengono le liste delle attività
#e delle emissioni del file in input, suddivise giorno per giorno.
def setup(filepath):
    with open(filepath, 'r') as f:
        days = [re.split(r' ',line)[0] for line in f][2:]
        days = sorted(list(set(days)))
    
    act_list=[[] for i in range(len(days))]
    obs_list=[[] for i in range(len(days))]
    
    with open(filepath, 'r') as f:
        for line in f:
            for day in days:
                if line.startswith(day):
                    act_list[days.index(day)].append(re.split(r'\t+\ *\t*',line.rstrip())[3])
                    obs_list[days.index(day)].append(re.split(r'\t+\ *\t*',line.rstrip())[2])
    
    return (act_list,obs_list)

#Stima del vettore delle probabilità iniziali normalizzate.
#Utilizza pseudocontatori per attività non osservate.
def init_prob(states, act_names):
    counts = [states.count(i) for i in act_names]
    for (i, value) in enumerate(counts):
        if value == 0:
            counts[i] = 1
    norm_init_prob = normal(counts)
    return norm_init_prob

#Stima della matrice di transizione con probabilità normalizzate.
#Utilizza pseudocontatori per transizioni non osservate.
def trans_prob(states, act_names):
    length = len(states)
    t_mat = [[0 for i in range(len(act_names))] for j in range(len(act_names))]
    for i in range(1,length):
        row = act_names.index(states[i-1])
        col = act_names.index(states[i])
        t_mat[row][col] += 1
    for l in t_mat:
        for (i, value) in enumerate(l):
            if value == 0:
                l[i] = 1
    norm_trans_prob = normal(t_mat)
    return norm_trans_prob

#Stima della matrice delle osservazioni con probabilità normalizzate.
#Utilizza pseudocontatori per emissioni non osservate.      
def ems_prob(states, observations, act_names, obs_names):
    length = len(states)
    ems_mat = [[0 for i in range(len(obs_names))] for j in range(len(act_names))]
    for i in range(length):
        row = act_names.index(states[i])
        col = obs_names.index(observations[i])
        ems_mat[row][col] += 1
    for l in ems_mat:
        for (i, value) in enumerate(l):
            if value == 0:
                l[i] = 1
    norm_ems_prob = normal(ems_mat)
    return norm_ems_prob

#Normalizzazione delle probabilità
def normal(lista):
    length = len(lista)
    norm = [0 for i in range(length)]
    if all([isinstance(x, list) for x in lista]):
        for i in range(length):
            norm[i] = normal(lista[i])
    else:
        if sum(lista)==0:
            norm = [0 for i in lista]
        else:
            norm = [float(i)/sum(lista) for i in lista]
    return norm

#Trasformazione da lista innestata a lista singola
def flatten(lists):
    flat = lambda l: [item for sublist in l for item in sublist]
    return flat(lists)

#Calcolo della differenza punto a punto tra due sequenze.
#Restituisce l'errore commesso in percentuale.
def seq_diff(seq,gt):
    c = 0
    for i in range(len(seq)):
        if seq[i] != gt[i]:
            c += 1
    error = c/len(seq) * 100
    return error

#Calcolo delle statistiche di performance.
#Restituisce il valore di f_measure in percentuale.
def score(seq,gt,act_names):
    conf_mat = [[0 for i in range(len(act_names))] for j in range(len(act_names))]
    for i in range(len(seq)):
        cur_act = seq[i]
        cur_gt = gt[i]
        conf_mat[act_names.index(cur_gt)][act_names.index(cur_act)] += 1
    true_pos = [conf_mat[i][i] for i in range(len(conf_mat))]
    total_true = [sum(row) if sum(row) != 0 else 1 for row in conf_mat]
    total_inferred = [sum(x) if sum(x) != 0 else 1 for x in zip(*conf_mat)]
    precision = sum([true_pos[i]/total_inferred[i] for i in range(len(conf_mat))])/len(conf_mat)
    recall = sum([true_pos[i]/total_true[i] for i in range(len(conf_mat))])/len(conf_mat)
    if (precision + recall) != 0:
        f_measure = (2 * precision * recall)/(precision + recall) * 100
    else:
        f_measure = 0
    return f_measure
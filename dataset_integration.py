import re
from datetime import datetime

activities_path = "C:/Users/Stefano/Desktop/2 - SmartHouse (HMM)/2 - SmartHouse (HMM)/UCI ADL Binary Dataset/OrdonezB_ADLs.txt"
sensors_path = "C:/Users/Stefano/Desktop/2 - SmartHouse (HMM)/2 - SmartHouse (HMM)/UCI ADL Binary Dataset/OrdonezB_Sensors.txt"

with open(activities_path, 'r') as activities_file,open(sensors_path, 'r') as sensors_file:
    activities_list = [re.split(r'\t+\ *\t*',str(line).rstrip()) for line in activities_file][2:]
    sensors_list = [re.split(r'\t+\ *\t*',str(line).rstrip()) for line in sensors_file][2:]

with open('C:/Users/Stefano/Desktop/OrdonezB_integrated2.txt', 'w') as integrated:
    integrated.write('Start Time\t\tEnd Time\t\tLocation\tActivity\n')
    integrated.write('----------\t\t--------\t\t--------\t--------\n')
    for act in activities_list:
        start_time = datetime.strptime(act[0].rstrip(),'%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(act[1].rstrip(),'%Y-%m-%d %H:%M:%S')
        activity = act[2].rstrip()
        for sen in sensors_list:
            start_obs = datetime.strptime(sen[0].rstrip(),'%Y-%m-%d %H:%M:%S')
            end_obs = datetime.strptime(sen[1].rstrip(),'%Y-%m-%d %H:%M:%S')
            location = sen[2].rstrip()
            if location == 'Door':
                place = sen[4].rstrip()
                if place == 'Living':
                    place = ' Bathroom'
                else:
                    place = ' '+ place
            else:
                place = ''
            if start_time <= start_obs and end_obs <= end_time:
                integrated.write('{}\t{}\t{}\t\t{}\n'.format(start_obs,end_obs,location+place,activity))
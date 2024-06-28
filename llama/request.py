### Request Class
import numpy as np
import datetime as dt
import json

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Request:
    def __init__(self, user_request, deltaT) -> None:
        self.user_request = user_request
        self.method = None
        self.t_i = None
        self.t_f = None
        self.T = None
        self.deltaT = deltaT
        self.N = None
        self.time_vector = None
        self.power = None

    def set_method(self, method):
        self.method = method
    
    def get_parser_message(self):
        return json.dumps({"prerequest":"Extract time parameters and call the solving method by generating the required parameters using your knowledge",
                "user_request":self.user_request,
                "current_date":dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    
    def set_duration(self, T):
        self.T = dt.timedelta(hours=T)
        self.t_f = self.t_i + self.T
        self.set_time_vector()
    
    def set_time_vector(self):
        '''Sets the time vector'''
        self.N = int(self.T / self.deltaT)
        self.time_vector = [self.t_i + i*self.deltaT for i in range(self.N+1)]

    def set_dates(self, t_i_str, t_f_str, T_str):
        '''Sets the initial and final dates'''
        if t_i_str == "None":
            t_i = dt.datetime.now()
            self.t_i = t_i.replace(hour=t_i.hour+1, minute=0, second=0, microsecond=0) if t_i.minute > 0 else t_i
        else:
            t_i = dt.datetime.strptime(t_i_str, '%Y-%m-%d %H:%M:%S')
            self.t_i = t_i.replace(hour=(t_i.hour+1)%23, minute=0, second=0, microsecond=0) if t_i.minute > 0 else t_i

        if t_f_str == "None":
            if T_str == "None":
                self.T = dt.timedelta(hours=10)
            else:
                self.T = dt.timedelta(hours=float(T_str))
            self.t_f = self.t_i + self.T
        else:
            t_f = dt.datetime.strptime(t_f_str, '%Y-%m-%d %H:%M:%S')
            self.t_f = t_f.replace(hour=(t_f.hour+1)%23, minute=0, second=0, microsecond=0) if t_f.minute > 0 else t_f

        self.T = self.t_f - self.t_i

        self.set_time_vector()

        return "{\"message\":'t_i, t_f and T are correctly set'}"

    def plot_power(self,axes):
        pow = self.power.tolist()
        pow += [0]*(48-len(pow)-1)
        pow.append(pow[-1])
        time = [self.t_i + i*self.deltaT for i in range(48)]
        #axes.step(self.time_vector, pow, where='post')
        axes.step(time, pow, where='post',linewidth=2)
        axes.set_xlabel("Time", fontsize=18)
        axes.set_ylabel("Power (kW)", fontsize=18)
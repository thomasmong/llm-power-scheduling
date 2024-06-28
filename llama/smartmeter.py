### SmartMeter class
import json
import numpy as np
import datetime as dt
from request import Request
import warnings
from gekko import GEKKO

from solver import Solver

class SmartMeter:

    def __init__(self, deltaT=.5):
        self.deltaT = dt.timedelta(hours=deltaT)
        self.day_duration = dt.timedelta(days=1)
        if self.day_duration % self.deltaT != dt.timedelta(0):
            raise Exception("The time step is not a divisor of the day duration")

        self.current_SOC = 0.3
        self.battery_capacity = 82
        self.max_charging_power = 22
        #self.current_temperature = 301
        #self.current_humidity = 0.5
        #self.max_HVAC_power = 1000
        #self.max_ventilation = 0.05
        self.set_vectors()

        # HVAC model parameters
        #self.set_HVAC_param()
    
    def set_vectors(self):
        '''Set the vectors for the hourly prices, power load and renewable factor'''
        N = int(self.day_duration / self.deltaT)
        self.hourly_prices = np.random.randint(1, 4, N)
        self.hourly_power_load = np.maximum(4*np.random.standard_normal(N) + 8,np.zeros(N))
        self.hourly_renew_factor = np.random.rand(N)
    
    def get_current_hour(self):
        return dt.datetime.now().hour
    
    def get_current_date(self,args=None):
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_incoming_prices(self,t_i:dt.datetime,T:dt.timedelta):
        extended_prices = np.tile(self.hourly_prices, 1 + int(T/self.day_duration))
        # Rotation
        extended_prices = np.roll(extended_prices, -t_i.hour)
        return extended_prices[:int(T.total_seconds()//self.deltaT.total_seconds())]

    def get_incoming_load(self,t_i:dt.datetime,T:dt.timedelta):
        extended_loads = np.tile(self.hourly_power_load, 1 + int(T/self.day_duration))
        # Rotation
        extended_loads = np.roll(extended_loads, -t_i.hour)
        return extended_loads[:int(T.total_seconds()//self.deltaT.total_seconds())]

    def get_incoming_renew_factor(self,t_i:dt.datetime,T:dt.timedelta):
        extended_renew_factor = np.tile(self.hourly_renew_factor, 1 + int(T/self.day_duration))
        # Rotation
        extended_renew_factor = np.roll(extended_renew_factor, -t_i.hour)
        return extended_renew_factor[:int(T.total_seconds()//self.deltaT.total_seconds())]
        
    def get_required_energy(self, final_SOC):
        '''Returns the required energy to reach the final SOC'''
        return np.array([(final_SOC - self.current_SOC) * self.battery_capacity])
    
    def pre_solve_LP(self, req, c_str, A_str='None', b_str='None', Aeq_str='None', beq_str='None', lb_str='None', ub_str='None'):
        '''Prepare the parameters for the LP solver and runs it.'''
        c = eval(c_str)
        A = eval(A_str)
        b = eval(b_str)
        Aeq = eval(Aeq_str)
        beq = eval(beq_str)
        lb = eval(lb_str)
        ub = eval(ub_str)
        return Solver.solve_LP(c,A,b,Aeq,beq,lb,ub)
    
    def pre_solve_MTL(self, req, A_str, B_str, xi_str, xf_str, Lu_str, Uu_str, Lx_str, Ux_str):
        '''Prepare the parameters for the MTL solver'''
        A = eval(A_str)
        B = eval(B_str)
        x_i = eval(xi_str)
        x_f = eval(xf_str)
        Lu = eval(Lu_str)
        Uu = eval(Uu_str)
        Lx = eval(Lx_str)
        Ux = eval(Ux_str)
        return Solver.solve_MTL(A,B,x_i,x_f,Lu,Uu,Lx,Ux)

    def pre_solve_MM(self, req, f_str, A_str="None", b_str="None", Aeq_str="None", beq_str="None", lb_str="None", ub_str="None"):
        '''Prepare the parameters for the MM solver'''
        def creer_lambdas(self,req):
            '''Create the lambda functions'''
            f = eval(f_str)
            n = len(f)
            fun = [lambda x,func=func: func(x) for func in f]
            return fun
        fun = creer_lambdas(self,req)
        A = eval(A_str)
        b = eval(b_str)
        Aeq = eval(Aeq_str)
        beq = eval(beq_str)
        lb = eval(lb_str)
        ub = eval(ub_str)
        return Solver.solve_MM(fun,A,b,Aeq,beq,lb,ub)

    def pre_solve_QP(self, req, Q_str, c_str, A_str='None', b_str='None', Aeq_str='None', beq_str='None', lb_str='None', ub_str='None'):
        '''Prepare the parameters for the QP solver and runs it.'''
        Q = eval(Q_str)
        c = eval(c_str)
        A = eval(A_str)
        b = eval(b_str)
        Aeq = eval(Aeq_str)
        beq = eval(beq_str)
        lb = eval(lb_str)
        ub = eval(ub_str)
        return Solver.solve_QP(Q,c,A,b,Aeq,beq,lb,ub)
    
    def pre_solve_DOP(self, req, J_str, f_str, Lu_str, Uu_str, Lx_str, Ux_str, x_i_str, x_f_str):
        '''Prepare the parameters for the DOP solver'''
        ## Model
        req.m, req.u, req.x, req.eqs = eval(f_str)

        ## Bounds
        req.Lu = eval(Lu_str)
        req.Uu = eval(Uu_str)
        req.Lx = eval(Lx_str)
        req.Ux = eval(Ux_str)

        # Initial and final conditions
        req.xi = eval(x_i_str)
        req.xf = eval(x_f_str)

        # Integral of J
        req.Jint = req.m.Var(0)
        req.m.Equation(req.Jint.dt() == eval(J_str))

        return self.solver.solve(req)
    
    def f(self, i, u, req):
        '''Workaround to use the function in the GEKKO model (MM solver)'''
        return eval(self.ff)
    
    def get_HVAC_model(self):
        '''Returns the HVAC model'''
        ## Define control and state
        m = GEKKO(remote=False)
        u = m.Array(m.Param, 2)
        x = m.Array(m.SV, 2)

        ## Equations
        eqs = []
        eqs.append(self.Cp*x[0].dt() == - (x[0]-self.T0) / self.R - self.eta*u[0])
        eqs.append(x[1].dt() == -x[1]*(1/x[0]**2*(self.b+2*self.c/x[0])*(self.eta*u[0]/self.Cp + (x[0]-self.T0)/(self.Cp*self.R))+(self.D0+u[1])/self.V) + (self.D0+u[1])/self.V*self.pv0/m.exp(self.a+self.b/x[0]+self.c/(x[0]**2)))

        return m, u, x, eqs

    def set_HVAC_param(self):
        '''Set the HVAC model parameters'''
        # Constants
        self.a = 23.3265
        self.b = - 3802.7
        self.c = - (472.68)**2
        self.e = 0.1 # meter
        self.lambda_ = 0.1 # W/m-K
        self.H = 2.80 # meter
        self.Ss = 100 # m2, surface area
        self.S = np.sqrt(self.Ss) * self.H # m2
        self.V = self.Ss*self.H # m^3
        self.R = self.e/(self.lambda_*self.S) # K/W
        self.C = 1256 # J/m3-K
        self.Cp = self.C*self.V # J/K
        self.tau = self.R*self.Cp # s
        self.Dmax = 0.05 # m3/s
        self.D0 = 0.0005 # m3/s, default air flow
        self.s = 0.05*0.05 # m2 ventilation area
        self.eta = 2 # efficiency of the air conditioning unit

        zero_abs = -273.18 # Celsius
        self.T0 = 38 - zero_abs# Kelvin
        self.h0 = 0.6 # Humidity outside
        Psat0 = np.exp(self.a + self.b / self.T0 + self.c / self.T0**2) # Pa
        self.pv0 = self.h0 * Psat0
from custom_agents.agents import ParserAgent
import time
import request
import datetime as dt
from smartmeter import SmartMeter
model = 'llama3-parser-LP'
requestt = "Please charge my car now for 8 hours at the lowest cost. I need the battery at 209%."
op_id = "LP"

parser = ParserAgent(model)
start = time.time()
output = parser.parse(requestt, verbose=True)
print(output)
time_function_call = output[0][0]
req = request.Request(requestt, dt.timedelta(hours=1))

t_i_str = time_function_call["arguments"]["t_i_str"]
t_f_str = time_function_call["arguments"]["t_f_str"]
T_str = time_function_call["arguments"]["T_str"]
req.set_dates(t_i_str, t_f_str,T_str)


solve_function_call = output[1][-1]
try:
    solve_args = solve_function_call["parameters"]
except:
    solve_args = solve_function_call["arguments"]

sm = SmartMeter(1)


solve_LP = lambda **kwargs: sm.pre_solve_LP(req,**kwargs)

res = solve_LP(**solve_args)
print(res)

# Real sol
'''
req_exp = request.Request(requestt, dt.timedelta(hours=1))
req_exp.set_dates(**expected_time)
expected_params = {'f_str': '[lambda x,self=self,req=req,i=i: x[i] + self.get_incoming_load(req.t_i,req.T)[i] for i in range(req.N)]',
                   'A_str': 'None',
                   'b_str': 'None',
                   'Aeq_str': '((req.deltaT / dt.timedelta(hours=1)) * np.ones(req.N).reshape(1,-1))',
                   'beq_str': 'self.get_required_energy(1)',
                   'lb_str': 'np.zeros(req.N)',
                   'ub_str': 'self.max_charging_power*np.ones(req.N)'}
res_exp = sm.pre_solve_MM(req_exp,**expected_params)
print(res_exp)

# Compare obj
obj = max(res+sm.get_incoming_load(req.t_i,req.T)) 
obj_exp = max(res_exp+sm.get_incoming_load(req_exp.t_i,req_exp.T))
'''

req_exp = request.Request(requestt, dt.timedelta(hours=1))
req_exp.set_dates(t_i_str, t_f_str,T_str)
expected_params = {'Q_str': '2*np.eye(req.N)',
                   'c_str': 'None',
                   'A_str': '-(req.deltaT / dt.timedelta(hours=1)) * np.ones(req.N).reshape(1,-1)',
                   'b_str': '-self.get_required_energy(1)',
                   'Aeq_str': 'None',
                   'beq_str': 'None',
                   'lb_str': 'np.zeros(req.N)',
                   'ub_str': 'self.max_charging_power * np.ones(req.N)'}
res_exp = sm.pre_solve_QP(req_exp,**expected_params)
print(res_exp)

# Compare obj
obj = max(res+sm.get_incoming_load(req.t_i,req.T)) 
obj_exp = max(res_exp+sm.get_incoming_load(req_exp.t_i,req_exp.T))
print(obj, obj_exp)
print((obj-obj_exp)/obj_exp)


print(f"Time taken: {time.time()-start:.2f} seconds")
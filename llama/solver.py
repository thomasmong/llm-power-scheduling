### Solver Class
import numpy as np
import scipy.optimize as opt
import cvxpy as cp

class Solver:

    def solve_LP(c, A=None, b=None, Aeq=None, beq=None, lb=None, ub=None):
        '''Solves the linear programming problem'''
        bds = [(lb[i], ub[i]) for i in range(len(c))]
        res = opt.linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=bds)
        if res.status == 0:
            return res.x
        return None
    
    def solve_QP(Q, c=None, A=None, b=None, Aeq=None, beq=None, lb=None, ub=None):
        '''Solves the quadratic programming problem'''
        if Q is None or np.linalg.norm(Q) == 0:
            print('Solving LP')
            return Solver.solve_LP(c, A, b, Aeq, beq, lb, ub)
        else:
            n = np.size(Q, 0)
            x = cp.Variable(n)
            if c is None:
                c = np.zeros(n)
            constraints = []
            if A is not None:
                constraints += [A @ x <= b]
            if Aeq is not None:
                constraints += [Aeq @ x == beq]
            if lb is not None:
                constraints += [lb[i] <= x[i] for i in range(n)]
            if ub is not None:
                constraints += [x[i] <= ub[i] for i in range(n)]

            prob = cp.Problem(cp.Minimize(0.5 * cp.quad_form(x, Q) + c @ x), constraints)
            prob.solve()
            return x.value


    def solve_MM(fun, A=None, b=None, Aeq=None, beq=None, lb=None, ub=None):
        '''Solves the mini-max problem'''
        g = [lambda x, f=f: f(x) - x[-1] for f in fun]
        x_0 =  np.zeros(np.size(Aeq, 1) + 1)
        if A is not None:
            A = np.hstack((A, np.ones((np.size(A, 0), 1))))
        if Aeq is not None:
            Aeq = np.hstack((Aeq, np.zeros((np.size(Aeq, 0), 1))))
        lb = np.append(lb, -np.inf)
        ub = np.append(ub, np.inf)
        res = Solver.solve_CP(lambda x: x[-1], x_0, g, A, b, Aeq, beq, lb, ub)
        return res[:-1]
    
    def solve_CP(f,x0,g=None,A=None,b=None,Aeq=None,beq=None,lb=None,ub=None):
        '''Solves the convex programming problem'''
        constraints = []
        if g is not None:
            for gi in g:
                constraints.append(opt.NonlinearConstraint(gi, -np.inf, 0))
        if A is not None:
            constraints.append(opt.LinearConstraint(A, ub=b))
        if Aeq is not None:
            constraints.append(opt.LinearConstraint(Aeq, beq, beq))
        if lb is not None and ub is not None:
            bounds = opt.Bounds(lb, ub)
        res = opt.minimize(f, x0, constraints=constraints, bounds=bounds, tol=1e-4)
        print(res.status,res.message)
        if res.status == 0:
            return res.x
        return None
    
    def solve_MTL(A, B, x_i, x_f, Lu=None, Uu=None, Lx=None, Ux=None, n=300):
        '''Solves the minimum time problem using MILP'''
        if type(A) is not np.ndarray:
            A = np.array(A).reshape(1,-1)
            B = np.array(B).reshape(1,-1)
            x_i = np.array(x_i).reshape(1,-1)
            x_f = np.array(x_f).reshape(1,-1)
            L_x = np.array(Lx).reshape(1,-1)
            U_x = np.array(Ux).reshape(1,-1)
        m = np.shape(A)[0]

        # Vector length
        l = 2*n + m * (n-1)

        # High constant
        C = 1e9

        # Objective
        c = np.zeros(l)
        c[n:2*n] = np.ones(n)

        # Int
        inte = c

        ## Constraints
        constraints = []
        Ain = np.empty((0,l))
        bin = np.empty(0)

        # Inequalities
        if Uu is not None:
            a = np.zeros((n,l))
            a[:,:n] = np.eye(n)
            a[:,n:2*n] = -Uu*np.eye(n)
            Ain = np.vstack((Ain, a))
            bin = np.hstack((bin, np.zeros(n)))
        
        if Lu is not None:
            a = np.zeros((n,l))
            a[:,:n] = -np.eye(n)
            a[:,n:2*n] = Lu*np.eye(n)
            Ain = np.vstack((Ain, a))
            bin = np.hstack((bin, np.zeros(n)))
        
        # \lambda_i >= \lambda_{i+1}
        a = np.zeros((n-1,l))
        a[:,n:2*n-1] = -np.eye(n-1)
        a[:,n+1:2*n] = a[:,n+1:2*n] + np.eye(n-1)
        Ain = np.vstack((Ain, a))
        bin = np.hstack((bin, np.zeros(n-1)))

        # \(-C\left( 1 - \lambda_k + \lambda_{k+1} \right) \leq \gamma_k \leq C\left( 1 - \lambda_k + \lambda_{k+1} \right)\)
        a = np.zeros((m*(n-1),l))
        a[:,n:2*n-1] = C*np.tile(np.eye(n-1), (m,1))
        a[:,n+1:2*n] = a[:,n+1:2*n] - C*np.tile(np.eye(n-1), (m,1))
        a[:,2*n:] = a[:,2*n:] + np.eye(m*(n-1))
        Ain = np.vstack((Ain, a))
        bin = np.hstack((bin, C*np.ones(m*(n-1))))

        a = np.zeros((m*(n-1),l))
        a[:,n:2*n-1] = C*np.tile(np.eye(n-1), (m,1))
        a[:,n+1:2*n] = a[:,n+1:2*n] - C*np.tile(np.eye(n-1), (m,1))
        a[:,2*n:] = a[:,2*n:] + np.eye(m*(n-1))
        Ain = np.vstack((Ain, a))
        bin = np.hstack((bin, C*np.ones(m*(n-1))))

        # State bounds
        if Lx is not None:
            al = np.zeros((m*n,l))
            bl = np.zeros(m*n)
            for k in range(2,n+2):
                D = np.zeros((m,n))
                for i in range(1,k):
                    D[:,i-1] = -np.power(A,k-i-1) @ B
                al[(k-2)*m:(k-1)*m,:n] = D
                bl[(k-2)*m:(k-1)*m] = np.power(A,k-1) @ x_i - Lx
            Ain = np.vstack((Ain, al))
            bin = np.hstack((bin, bl))
        if Ux is not None:
            au = np.zeros((m*n,l))
            bu = np.zeros(m*n)
            for k in range(2,n+2):
                D = np.zeros((m,n))
                for i in range(1,k):
                    D[:,i-1] = np.power(A,k-i-1) @ B
                au[(k-2)*m:(k-1)*m,:n] = D
                bu[(k-2)*m:(k-1)*m] = Ux - np.power(A,k-1) @ x_i
            Ain = np.vstack((Ain, au))
            bin = np.hstack((bin, bu))
        
        constraints.append(opt.LinearConstraint(Ain, ub=bin))
        
        # Equality constraints
        a1 = np.zeros((1,l))
        a1[:,n] = 1
        b1 = 1

        aq = np.zeros((m*(n-1),l))
        bq = np.zeros(m*(n-1))

        for k in range(2,n+1):
            D = np.zeros((m,n))
            for i in range(1,k):
                D[:,i-1] = np.power(A,k-i-1) @ B
            aq[(k-2)*m:(k-1)*m,:n] = D
            bq[(k-2)*m:(k-1)*m] = -np.power(A,k-1) @ x_i + x_f
            h = np.zeros((m,m*(n-1)))
            for j in range(1,m+1):
                h[j-1,k-2+(j-2)*(n-1)] = 1
            aq[(k-2)*m:(k-1)*m,2*n:] = h
        
        Aeq = np.vstack((a1,aq))
        beq = np.hstack((b1,bq))

        constraints.append(opt.LinearConstraint(Aeq, beq, beq))

        ## Control Bounds
        lb1 = -np.inf*np.ones(n)
        lb2 = np.zeros(n)
        lb3 = -np.inf*np.ones(m*(n-1))
        lb = np.hstack((lb1,lb2,lb3))

        ub1 = np.inf*np.ones(n)
        ub2 = np.ones(n)
        ub3 = np.inf*np.ones(m*(n-1))
        ub = np.hstack((ub1,ub2,ub3))

        # Solve
        res = opt.milp(c, integrality=inte, constraints=constraints, bounds=opt.Bounds(lb, ub))

        if res.status == 0:
            T = int(np.sum(res.x[n:2*n]))
            u = res.x[:T]
            return u
        else:
            return None


# Test
if __name__ == '__main__':
    n = 5
    c = -np.random.rand(n)
    lb = np.zeros(n)
    ub = 1*np.ones(n)
    Q = np.zeros((n,n))
    A = -np.array([1,1,1,1,1]).reshape(1,-1)
    b = -3
    
    print(Solver.solve_LP(c, A, b, lb=lb, ub=ub))
    print(Solver.solve_QP(Q, c, A, b, lb=lb, ub=ub))

    Q = np.random.rand(n,n)
    Q = Q @ Q.T
    print(Solver.solve_QP(Q, c, A, b, lb=lb, ub=ub))

    C = np.eye(n)
    d = -np.random.randint(0,5,n)
    print(d)
    print(Solver.solve_LMM(C, d, A, b, lb=lb, ub=ub))


    # Test MT
    print("Test MT")
    T = 7
    Q = 10
    Pm = 10/T
    A = 1
    B = 1/Q
    x_i = 0
    x_f = 1
    Lu = 0
    Uu = Pm
    Lx = 0
    Ux = 1

    res = Solver.solve_MT(A, B, x_i, x_f, Lu, Uu, Lx, Ux, n=10)
    if res is not None:
        print(res)

    # Test CP
    print("Test CP")
    f = lambda x: 100*(x[1] - x[0]**2)**2 + (1 - x[0])**2
    g1 = lambda x: x[0] + 2*x[1] - 1
    g2 = lambda x: x[0]**2 + x[1] - 1
    g3 = lambda x: x[0]**2 - x[1] - 1
    A = np.array([2, 1]).reshape(1,-1)
    b = 1
    lb = np.array([-1,-1])
    ub = np.array([1,2])

    res = Solver.solve_CP(f, [0,0], [g1,g2,g3], A, b, lb=lb, ub=ub)
    print(res)
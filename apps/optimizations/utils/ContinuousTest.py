import pulp

class VertiportLP:
    def __init__(self, mf, mpi, mpo, mg, mn, cfi, cfo, cpi, cpo, cg, cn, cm, wt, wu):
        self.mf = mf
        self.mpi = mpi
        self.mpo = mpo
        self.mg = mg
        self.mn = mn
        self.cfi = cfi
        self.cfo = cfo
        self.cpi = cpi
        self.cpo = cpo
        self.cg = cg
        self.cn = cn
        self.cm = cm
        self.wt = wt
        self.wu = wu

        # 의사결정 변수:
        #  sfi: fato로 착륙을 준비하는 UAM의 점유율 (0에서 1 사이의 연속적인 값을 가짐)
        #  sfo: fato에서 이륙을 준비하는 UAM의 점유율 (0에서 1 사이의 연속적인 값을 가짐)
        #  spi: path_in의 UAM 점유율 (0에서 1 사이의 연속적인 값을 가짐)
        #  spo: path_out의 UAM 점유율 (0에서 1 사이의 연속적인 값을 가짐)
        #  sg: gate의 UAM 점유율 (0에서 1 사이의 연속적인 값을 가짐)
        #  sn: 대합실에 있는 인원 수 (정수값)
        #  sm: gate의 UAM 탑승 인원 수 (정수값, 최대값은 mg(게이트 수) * 4)

        self.sfi = pulp.LpVariable('sfi', lowBound=0, upBound=1, cat='Continuous')
        self.sfo = pulp.LpVariable('sfo', lowBound=0, upBound=1, cat='Continuous')
        self.spi = pulp.LpVariable('spi', lowBound=0, upBound=1, cat='Continuous')
        self.spo = pulp.LpVariable('spo', lowBound=0, upBound=1, cat='Continuous')
        self.sg = pulp.LpVariable('sg', lowBound=0, upBound=1, cat='Continuous')
        self.sn = pulp.LpVariable('sn', lowBound=0, upBound=self.mn, cat='Integer')
        self.sm = pulp.LpVariable('sm', lowBound=0, upBound=self.mg * 4, cat='Integer')

        self.w1, self.w2, self.w3, self.w4, self.w5, self.w6 = (0.04, 0.02, 0.38, 0.31, 0.1, 0.15) # w1 ~ w5의 합은 1
        self.w7, self.w8, self.w9, self.w10 = (0.31, 0.20, 0.2, 0.29) # w7 ~ w10의 합은 1

    def set_problem(self) -> pulp.LpProblem:
        problem = pulp.LpProblem("UAM_Optimization", pulp.LpMinimize)

        C = self.w1 * self.sfi + self.w2 * self.spi + self.w3 * self.sg + self.w4 * self.spo + self.w5 * self.sfo + self.w6 * self.sn
        U = self.w7 * self.sg + self.w8 * self.spo + self.w9 * self.sfo + self.w10 * self.sm

        problem += (C - self.wu * U)

        # 식하나하나 무슨 의미인지 이해가 안되니 다 적어보자.
        # 제약조건 1: sfi와 sfo의 합이 1 이하여야 함.
        problem += self.sfi + self.sfo <= 1

        # 제약조건 2: sm은 4 * (sg * mg) 이하여야 함.
        problem += self.sm <= 4 * (self.sg * self.mg)

        # 제약조건 3: fato로 착륙을 준비하는 UAM과 fato에서 이륙을 준비하는 UAM의 점유율에 대한 가중치가 곱해진 값, 
        # path_in의 UAM 점유율에 대한 가중치가 곱해진 값, gate의 UAM 점유율에 대한 가중치가 곱해진 값, 
        # path_out의 UAM 점유율에 대한 가중치가 곱해진 값의 합이 현재 상태의 fato로 착륙을 준비하는 UAM의 수, 
        # 현재 상태의 path_in의 UAM의 수, 현재 상태의 gate의 UAM의 수, 현재 상태의 path_out의 UAM의 수와 같아야 함.
        problem += (self.sfi + self.sfo) * self.mf + self.spi * self.mpi + self.sg * self.mg + self.spo * self.mpo == self.cfi + self.cpi + self.cg + self.cpo

        # 제약조건 4: 현재 상태의 path_out에 있는 UAM과 현재 상태의 fato에서 이륙을 준비하는 UAM의 수에 4를 곱한 값,
        # gate의 UAM 탑승 인원 수, 대합실에 있는 인원 수가 
        # 현재 상태의 path_out에 있는 UAM의 수와 현재 상태의 fato에서 이륙을 준비하는 UAM의 수의 합에 4를 곱한 값,
        # gate의 UAM 탑승 인원 수, 대합실에 있는 인원 수와 같아야 함.
        problem += 4 * (self.spo * self.mpo + self.sfo * self.mf) + self.sm + self.sn == 4 * (self.cpo + self.cfo) + self.cm

        # 제약조건 5: 현재 상태의 path_out에 있는 UAM과 현재 상태의 fato에서 이륙을 준비하는 UAM의 수에 4를 곱한 값과
        # gate의 UAM 탑승 인원 수는 현재 상태의 gate의 UAM 탑승 인원 수와 같거나 커야 함.
        problem += 4 * (self.spo * self.mpo + self.sfo * self.mf) + self.sm >= self.cm

        # 제약조건 6: fato로 착륙을 준비하는 UAM과 path_in의 UAM의 점유율에 대한 가중치가 곱해진 값의 합이
        # 현재 상태의 fato로 착륙을 준비하는 UAM의 수와 현재 상태의 path_in의 UAM의 수와 같거나 작아야 함.
        problem += self.sfi * self.mf + self.spi * self.mpi <= self.cfi + self.cpi

        # 제약조건 7: path_out의 UAM 점유율과 fato에서 이륙을 준비하는 UAM의 점유율에 대한 가중치가 곱해진 값의 합이
        # 현재 상태의 path_out의 UAM의 수와 현재 상태의 fato에서 이륙을 준비하는 UAM의 수와 같거나 크거나 같아야 함.
        problem += self.spo * self.mpo + self.sfo * self.mf >= self.cpo + self.cfo


        return problem

    def solve(self):
        problem = self.set_problem()
        problem.solve()

        solution = {}
        for var in problem.variables():
            solution[var.name] = var.varValue

        solution['Objective'] = pulp.value(problem.objective)

        return solution

#for debugging

# 매개변수 및 상수 설정
mf = 4          # fato의 UAM 최대 수용량 (대)
mpi = 6         # path_in의 UAM 최대 수용량 (대)
mpo = 6         # path_out의 UAM 최대 수용량 (대)
mg = 8          # gate의 UAM 최대 수용량 (대)
mn = 100        # waiting_room의 최대 수용 가능 인원 (명)
cfi = 2         # 현재 fato로 착륙을 준비하는 UAM의 수 (대)
cfo = 0         # 현재 fato에서 이륙을 준비하는 UAM의 수 (대)
cpi = 6         # 현재 path_in에 있는 UAM의 수 (대)
cpo = 2         # 현재 path_out에 있는 UAM의 수 (대)
cg = 3          # 현재 gate에 있는 UAM의 수 (대)
cn = 40         # 현재 waiting_room에 있는 사람의 수 (명)
cm = 7          # 현재 gate에서의 UAM 탑승 인원 (명)
wt = 0.5        # 계산에 사용되는 가중치
wu = 0.5        # 전체 이용률에 대한 가중치

lp_solver = VertiportLP(mf, mpi, mpo, mg, mn, cfi, cfo, cpi, cpo, cg, cn, cm, wt, wu)
solution = lp_solver.solve()

print("Solution:")
for var_name, var_value in solution.items():
    print(f"{var_name}: {var_value}")
print(f"Objective: {solution['Objective']}")

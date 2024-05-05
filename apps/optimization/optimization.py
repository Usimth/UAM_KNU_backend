import pulp

class vertiport:
    
    def __init__(self,weight) -> None:
        self.max_fato_uam = 4
        self.max_path_in_uam = 6
        self.max_path_out_uam = 6
        self.max_gate_uam = 8
        self.max_gate_psg = 55
        
        self.current_fato_in_uam = 3
        self.current_path_in_uam = 6
        self.current_gate_uam = 1
        self.current_path_out_uam = 3
        self.current_fato_out_uam = 0
        self.current_gate_psg = 34
        self.current_uam_psg = 9
        self.weight = weight
        
        #의사결정 변수
        self.x_fato_in_uam = pulp.LpVariable('x_fato_in_uam',lowBound=0,upBound=self.max_fato_uam,cat='Integer')
        self.x_path_in_uam = pulp.LpVariable('x_path_in_uam',lowBound=0,upBound=self.max_path_in_uam,cat='Integer')
        self.x_gate_uam = pulp.LpVariable('x_gate_uam',lowBound=0,upBound=self.max_gate_uam,cat='Integer')
        self.x_gate_psg = pulp.LpVariable('x_gate_psg',lowBound=0,upBound=self.max_gate_psg,cat='Integer')
        self.x_uam_psg = pulp.LpVariable('x_uam_psg',lowBound=0,upBound=4*self.max_gate_uam,cat='Integer')
        self.x_path_out_uam = pulp.LpVariable('x_path_out_uam',lowBound=0,upBound=self.max_path_out_uam,cat='Integer')
        self.x_fato_out_uam = pulp.LpVariable('x_fato_out_uam',lowBound=0,upBound=self.max_fato_uam,cat='Integer')
        
        self.w1, self.w2, self.w3, self.w4, self.w5 = (0.15, 0.1, 0.35, 0.3, 0.1)
        self.w6, self.w7, self.w8, self.w9 = (0.2, 0.27, 0.3, 0.33)
        
    def get_congestion(self) :
        congest = self.w1 * self.x_fato_in_uam.varValue / self.max_fato_uam  \
            + self.w2 * self.x_path_in_uam.varValue/ self.max_path_in_uam \
            + self.w3 * self.x_gate_uam.varValue / self.max_gate_uam \
            + self.w4 * self.x_path_out_uam.varValue / self.max_path_out_uam \
            + self.w5 * self.x_fato_out_uam.varValue / self.max_fato_uam
        return congest
    
    def get_using (self):
        using = self.w6 * ((self.x_path_out_uam.varValue + self.x_fato_out_uam.varValue)*4 + self.x_uam_psg.varValue) / self.max_gate_psg \
            + self.w7 * self.x_gate_uam.varValue / self.max_gate_uam \
            + self.w8 * self.x_path_out_uam.varValue / self.max_path_out_uam \
            + self.w9 * self.x_fato_out_uam.varValue / self.max_fato_uam
            
        return using

    def set_problem(self) -> pulp.LpProblem:
        congest = self.w1 * self.x_fato_in_uam / self.max_fato_uam  \
            + self.w2 * self.x_path_in_uam/ self.max_path_in_uam \
            + self.w3 * self.x_gate_uam / self.max_gate_uam \
            + self.w4 * self.x_path_out_uam / self.max_path_out_uam \
            + self.w5 * self.x_fato_out_uam / self.max_fato_uam
        using = self.w6 * ((self.x_path_out_uam + self.x_fato_out_uam)*4 + self.x_uam_psg) / self.max_gate_psg \
            + self.w7 * self.x_gate_uam / self.max_gate_uam \
            + self.w8 * self.x_path_out_uam / self.max_path_out_uam \
            + self.w9 * self.x_fato_out_uam / self.max_fato_uam
        weight = self.weight
        problem = pulp.LpProblem("UAM_Optimization", pulp.LpMinimize)
        problem += congest-(weight)*using

        #전체 UAM 대수는 동일
        problem += self.x_fato_in_uam + self.x_fato_out_uam + self.x_path_in_uam + self.x_path_out_uam + self.x_gate_uam ==  self.current_gate_uam + self.current_path_in_uam + self.current_path_out_uam + self.current_fato_in_uam + self.current_fato_out_uam

        #전체 인원도 동일
        problem += (self.x_path_out_uam + self.x_fato_out_uam)*4 + self.x_uam_psg + self.x_gate_psg == (self.current_path_out_uam + self.current_fato_out_uam)*4 + self.current_uam_psg + self.current_gate_psg

        #대기자 수는 같거나 줄어듦
        problem += self.x_gate_psg <= self.current_gate_psg

        #현재 탑승 중인 사람은 4명 채워져서 출발하거나 그대로 대기
        problem += (self.x_path_out_uam + self.x_fato_out_uam)*4 + self.x_uam_psg >= self.current_uam_psg

        #fato_in + path_in의 UAM 대수는 같거나 줄어들 수 밖에 없음
        problem += self.x_fato_in_uam + self.x_path_in_uam <= self.current_fato_in_uam + self.current_path_in_uam

        #path_out + fato_out의 UAM 대수는 같거나 늘어날 수 밖에 없음
        problem += self.current_fato_out_uam + self.current_path_out_uam <= self.x_fato_out_uam + self.x_path_out_uam

        #이/착륙지
        problem += self.current_fato_out_uam <= self.x_fato_out_uam
        problem += self.current_fato_in_uam >= self.x_fato_in_uam
        problem += self.x_fato_in_uam + self.x_fato_out_uam <= self.max_fato_uam

        #UAM 탑승자 limit
        problem += self.x_uam_psg <= self.x_gate_uam*4
        return problem

        
        
    
    def optimizing(self) :
        problem = self.set_problem()
        problem.solve()
        
        solution = {}
        
        for var in problem.variables():
            solution[var.name] = var.varValue
        solution['congestion'] = self.get_congestion()
        solution['using'] = self.get_using()
        
        return solution
        
        
        
        
        
        
        
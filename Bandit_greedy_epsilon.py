#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:48:06 2021

@author: delizhu
"""
import numpy as np
import matplotlib.pyplot as plt

class Bandit:
    def __init__(self):
        self.arm_values = np.random.normal(0,1,10) ## 各臂收益的真实值
        self.K = np.zeros(10) ## K = 10 个臂
        self.est_values = np.zeros(10)

    def get_reward(self,action):
        noise = np.random.normal(0,0.1)
        reward = self.arm_values[action] + noise   ## 给获取的汇报加入噪声
        return reward
    def choose_eps_greedy(self,epsilon):           ##选择 action
        rand_num = np.random.random()
        if rand_num < epsilon:
            return np.random.randint(10)
        else:
            return np.argmax(self.est_values)
        
    def update_est(self,action,reward):           ## update est_values 更新action所选臂的估计收益
        self.K[action] += 1
        alpha = 1/self.K[action]
        self.est_values[action] += alpha *(reward - self.est_values[action])
        
def Experiment(bandit,Npulls,epsilon):
    step_reward = []
    avgacc_reward = [0]
    for i in range(Npulls):
        action = bandit.choose_eps_greedy(epsilon)
        R = bandit.get_reward(action)
        bandit.update_est(action,R)
        step_reward.append(R)                                ## 记录每一步收益
        avgacc_reward.append((i*avgacc_reward[-1]+R)/(i+1))  ## 记录累积平均收益
    return [np.array(step_reward),np.array(avgacc_reward[1:])]


### 进行多次实验取平均step_reward 和 avgacc_reward
### 设置eps = 0, 0.1, 0.01
Npulls = 300 #摇臂次数
Nexp = 200 #试验次数
avg_outcome_eps0p0 = np.zeros(Npulls)
avg_outcome_eps0p1 = np.zeros(Npulls)
avg_outcome_eps0p01 = np.zeros(Npulls)
avg_avgacc_eps0p0 = np.zeros(Npulls)
avg_avgacc_eps0p1 = np.zeros(Npulls)
avg_avgacc_eps0p01 = np.zeros(Npulls)


for i in range(Nexp):
    bandit = Bandit()
    [step_reward,avgacc_reward] = Experiment(bandit,Npulls,0.0)
    avg_outcome_eps0p0 += step_reward
    avg_avgacc_eps0p0 += avgacc_reward
    
    bandit = Bandit()
    [step_reward,avgacc_reward] = Experiment(bandit,Npulls,0.1)
    avg_outcome_eps0p1 += step_reward
    avg_avgacc_eps0p1 += avgacc_reward
    
    bandit = Bandit()
    [step_reward,avgacc_reward] = Experiment(bandit,Npulls,0.01)
    avg_outcome_eps0p01 += step_reward
    avg_avgacc_eps0p01 += avgacc_reward
    
avg_outcome_eps0p0 /= np.float(Nexp)
avg_outcome_eps0p1 /= np.float(Nexp)
avg_outcome_eps0p01 /= np.float(Nexp)
avg_avgacc_eps0p0 /= np.float(Nexp)
avg_avgacc_eps0p1 /= np.float(Nexp)
avg_avgacc_eps0p01 /= np.float(Nexp)

    

plt.plot(avg_outcome_eps0p0, label ='step avg outcome ,eps = 0.0')
plt.plot(avg_outcome_eps0p1, label ='step avg outcome ,eps = 0.1')
plt.plot(avg_outcome_eps0p01, label ='step avg outcome ,eps = 0.01')
plt.plot(avg_avgacc_eps0p0, label ='avgacc  ,eps = 0.0')
plt.plot(avg_avgacc_eps0p1, label ='avgacc  ,eps = 0.1')
plt.plot(avg_avgacc_eps0p01, label ='avgacc  ,eps = 0.01')

plt.ylim = (0,2.5)
plt.legend()
plt.show()
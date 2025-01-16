from math import inf

def translate_list(dic, vals):
    return [dic.get(x, "null") for x in vals]

def solve(coins, max_val, dic):
    sol_len = [inf for k in range(max_val +1)]
    sol_list = [[] for k in range(max_val +1)]
    
    sol_len[0] = 0
    
    for coin in coins:
        if coin > 0:
            sol_len[coin] = 1
            sol_list[coin] = [coin]
    
    for coin in coins:
        for i in range(0, max_val):
            #Outside of range [0,max_val]
            if coin + i > max_val or coin + i < 1:
                continue
            if sol_len[i+coin] > sol_len[i] + 1:
#                if sum(sol_list[i] + [coin]) != i+coin:
#                    continue
                sol_len[i+coin] = sol_len[i] + 1;
                sol_list[i+coin] = sol_list[i] + [coin]
                
    for i in range(0, max_val):
        sol_list[i].sort()
        print(f"-{i}:{sol_len[i]} {[-x for x in sol_list[i]]}\n\t{translate_list(dic, sol_list[i])}")
        
    
# + right, - left
coins = [-2, -7, -13, -16, 3, 6, 9, 15]
names = {-2: "punch", -7:"bend",-13:"upset",-16:"shrink",3:"light hit",6:"medium hit",9:"heavy hit",15:"draw"}
solve(coins, 150, names)

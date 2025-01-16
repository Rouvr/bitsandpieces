from math import inf

def translate_list(dic, vals):
    return [dic.get(x, "null") for x in vals]

def find_hits(target):
    # Define actions and names based on target direction
    if target >= 0:
        coins = [2, 7, 13, 16, -3, -6, -9, -15]
        names = {
            2: "punch", 7: "bend", 13: "upset", 16: "shrink",
            -3: "light hit", -6: "medium hit", -9: "heavy hit", -15: "draw"
        }
    else:
        coins = [-2, -7, -13, -16, 3, 6, 9, 15]
        names = {
            -2: "punch", -7: "bend", -13: "upset", -16: "shrink",
            3: "light hit", 6: "medium hit", 9: "heavy hit", 15: "draw"
        }

    abs_target = abs(target)

    # Initialize solution arrays with size based on target
    max_val = abs_target + max(abs(min(coins)), abs(max(coins))) + 1
    sol_len = [inf for _ in range(max_val)]
    sol_list = [[] for _ in range(max_val)]

    sol_len[0] = 0

    # Dynamic programming to find solutions
    for i in range(max_val):
        for coin in coins:
            next_val = i + coin
            if 0 <= next_val < max_val:
                if sol_len[next_val] > sol_len[i] + 1:
                    sol_len[next_val] = sol_len[i] + 1
                    sol_list[next_val] = sol_list[i] + [coin]

    # Get solution for target
    if sol_len[abs_target] == inf:
        return "No solution exists"

    solution = sol_list[abs_target]
    solution.sort()

    return f"Target {target}:\nActions ({sol_len[abs_target]} hits): {solution}\nNames: {translate_list(names, solution)}"

# Example usage
if __name__ == "__main__":
    import sys
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print(find_hits(target))

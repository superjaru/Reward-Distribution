def reward_distribute(events: list[tuple[str,int,int]]) -> dict[str, float]:
    #formula  reward = (user_share/total_shares ) * (duration * reward_rate) 
    events.sort(key=lambda x: x[1])
    result = {}
    total_shares = {} # total shares each user {'A' : allshares}
    reward_rate = 2.778
    time_limit = 3600
    tokens = 10000
    last_timestamp = 0
    for user, timestamp, share_adjust in events:
        if timestamp >= time_limit :
             share_adjust = 0
        duration = timestamp - last_timestamp
        last_timestamp = timestamp
        for u in total_shares :
            if sum(total_shares.values()) == 0 :
                continue
            else : result[u] = result.get(u,0) + (total_shares[u])/ sum(total_shares.values())  * (duration * reward_rate)
            # print(result , total_shares , duration)    
        total_shares[user] = total_shares.get(user, 0) + share_adjust
        if total_shares[user] < 0:
            total_shares[user] = 0
        tokens -= duration * reward_rate
        if tokens <= 0:
            break

    #calculate the rest
    for u in total_shares :   
            if sum(total_shares.values()) == 0 :
                 return result 
            else : result[u] = result.get(u,0) + (total_shares[u])/ sum(total_shares.values()) * tokens
    return result




#test cases

# print(reward_distribute([("A", 0, 2), ("B", 3605, 1), ("A", 10, -2)]))
test_cases = [
    ([], {}),   #Test case 1 
    ([("A", 0, 2), ("B", 2, 1), ("A", 10, -1)],{'A': 5006.482, 'B': 4993.518}), #Test case 2
    ([("A", 0, 5)], {'A': 10000.0}), #Test case 3
    ([("A", 0, 5), ("B", 0, 5)], {'A': 5000.0, 'B': 5000.0}), #Test case 4
    ([("A", 0, 5), ("B", 100, 5), ("A", 200, -5)], {'A': 416.7, 'B': 9583.3}), #Test case 5
    ([("A", 0, 5), ("B", 100, 5), ("A", 200, -5), ("B", 300, -5)], {'A': 416.7, 'B': 416.7}),  #Test case 6
    ([("A", 0, 0), ("B", 2, 0)], {}),  #Test case 7
    ([("A", 0, 5), ("A", 10, -5), ("A", 20, 5)], {'A': 9972.22}),  #Test case 8
    ([("A", 0, 5), ("A", 10, -5), ("A", 20, 5), ("B", 3600, 5)], {'A': 9972.22}),  #Test case 9
    ([("A", 0, 5), ("A", 10, -5), ("A", 20, 5), ("B", 3599, 5)], {'A': 9970.831 , 'B' : 1.389}),  #Test case 10
]

for i, (events, expected_output) in enumerate(test_cases):
    result = reward_distribute(events)
    for k in expected_output:
        assert abs(result.get(k, 0) - expected_output[k]) < 0.81, f"Test case {i+1} failed for user {k}: expected {expected_output[k]}, got {result.get(k, 0)}"
    print(f"Test case {i+1} passed.")

print("All test cases passed!")
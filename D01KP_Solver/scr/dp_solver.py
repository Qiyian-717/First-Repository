import time
import numpy as np


def sort_item_sets_by_ratio(item_sets):
    """按项集第三项价值重量比非递增排序（保持不变）"""

    def ratio(item_set):
        v3, w3 = item_set[2][0], item_set[2][1]
        return v3 / (w3 + 1e-6)

    return sorted(item_sets, key=ratio, reverse=True)


def dynamic_programming_solve(cubage, item_sets):
    """
    NumPy 向量化加速版动态规划   :param cubage: 背包容量    :param item_sets: 项集列表  :return: 最优解字典
    """
    N = len(item_sets)
    start_time = time.time()
    # ===== 阶段1：用 NumPy 一维 DP 数组，向量化更新 =====
    dp = np.zeros(cubage + 1, dtype=np.int32)  # 用 int32 节省内存，加速计算
    for i in range(N):
        v0, w0 = item_sets[i][0]
        v1, w1 = item_sets[i][1]
        v2, w2 = item_sets[i][2]
        # 向量化计算三种选择的候选值（避免 Python 内层循环）
        if w0 <= cubage:
            cand0 = np.concatenate([np.zeros(w0, dtype=np.int32), dp[:-w0] + v0])
        else:
            cand0 = dp
        if w1 <= cubage:
            cand1 = np.concatenate([np.zeros(w1, dtype=np.int32), dp[:-w1] + v1])
        else:
            cand1 = dp
        if w2 <= cubage:
            cand2 = np.concatenate([np.zeros(w2, dtype=np.int32), dp[:-w2] + v2])
        else:
            cand2 = dp

        # 向量化取 max：一次完成所有重量的更新
        dp = np.max([dp, cand0, cand1, cand2], axis=0)

    # ===== 阶段2：反向回溯路径（和之前逻辑一致，只做一次）=====
    optimal_value = int(dp[cubage])
    optimal_weight = 0
    optimal_choice = []
    current_w = cubage

    for i in range(N - 1, -1, -1):
        v0, w0 = item_sets[i][0]
        v1, w1 = item_sets[i][1]
        v2, w2 = item_sets[i][2]
        choice = -1

        if current_w >= w2 and dp[current_w] == dp[current_w - w2] + v2:
            choice = 2
            optimal_weight += w2
            current_w -= w2
        elif current_w >= w1 and dp[current_w] == dp[current_w - w1] + v1:
            choice = 1
            optimal_weight += w1
            current_w -= w1
        elif current_w >= w0 and dp[current_w] == dp[current_w - w0] + v0:
            choice = 0
            optimal_weight += w0
            current_w -= w0
        optimal_choice.append(choice)

    optimal_choice.reverse()
    solve_time = round(time.time() - start_time, 2)

    return {
        'optimal_value': optimal_value,
        'optimal_weight': optimal_weight,
        'optimal_choice': optimal_choice,
        'solve_time': solve_time
    }


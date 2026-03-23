import pandas as pd


def save_result_to_txt(result, dataset_name, cubage, save_path):
    """
    保存结果到TXT文件
    :param result: 求解结果字典
    :param dataset_name: 数据集名称
    :param cubage: 背包容量
    :param save_path: 保存路径
    """
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(f"=== D{0 - 1}KP 求解结果 ===\n")
            f.write(f"数据集名称：{dataset_name}\n")
            f.write(f"背包容量：{cubage}\n")
            f.write(f"最优总价值：{result['optimal_value']}\n")
            f.write(f"最优总重量：{result['optimal_weight']}\n")
            f.write(f"求解耗时：{result['solve_time']}秒\n")
            f.write(f"项集最优选择（-1=不选，0=物品0，1=物品1，2=物品2）：\n")
            f.write(str(result['optimal_choice']) + "\n")
        return True
    except Exception as e:
        raise Exception(f"TXT保存失败：{str(e)}")


def export_result_to_excel(result, dataset_name, cubage, item_sets, save_path):
    """
    导出结果到Excel文件
    :param result: 求解结果字典
    :param dataset_name: 数据集名称
    :param cubage: 背包容量
    :param item_sets: 项集列表
    :param save_path: 保存路径
    """
    try:
        # 基础信息表
        basic_info = pd.DataFrame({
            '参数': ['数据集名称', '背包容量', '最优总价值', '最优总重量', '求解耗时(秒)'],
            '值': [
                dataset_name,
                cubage,
                result['optimal_value'],
                result['optimal_weight'],
                result['solve_time']
            ]
        })

        # 项集选择详情表
        choice_info = []
        for i, choice in enumerate(result['optimal_choice']):
            if choice == -1:
                v, w = 0, 0
            else:
                v, w = item_sets[i][choice][0], item_sets[i][choice][1]
            choice_info.append({
                '项集序号': i + 1,
                '最优选择': choice,
                '选择物品价值': v,
                '选择物品重量': w
            })
        choice_df = pd.DataFrame(choice_info)

        # 写入Excel
        with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
            basic_info.to_excel(writer, sheet_name='基础信息', index=False)
            choice_df.to_excel(writer, sheet_name='项集选择详情', index=False)
        return True
    except Exception as e:
        raise Exception(f"Excel导出失败：{str(e)}")
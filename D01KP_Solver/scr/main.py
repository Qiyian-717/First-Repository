import os
import glob
from data_loader import parse_d01kp_file, get_dataset_list, get_dataset_detail
from dp_solver import sort_item_sets_by_ratio, dynamic_programming_solve
from plot_draw import draw_scatter_plot
from file_saver import save_result_to_txt, export_result_to_excel


def load_all_data_files(data_dir="../data"):
    """
    自动加载data文件夹下所有txt数据文件（给数据集加文件前缀，避免名称覆盖）
    :param data_dir: data文件夹路径（默认../data，即scr的上级目录下的data）
    :return: 合并后的所有数据集字典
    """
    all_data = {}
    # 扫描data文件夹下所有txt文件
    txt_files = glob.glob(os.path.join(data_dir, "*.txt"))
    if not txt_files:
        raise Exception(f"在{data_dir}下未找到任何txt数据文件！")

    print(f"找到{len(txt_files)}个数据文件：")
    for file in txt_files:
        print(f"- {os.path.basename(file)}")
    print()

    # 逐个解析并合并数据集（加文件前缀）
    for file in txt_files:
        try:
            file_data = parse_d01kp_file(file)
            # 提取文件名前缀（如wdkp1-10.txt → wdkp1-10）
            file_prefix = os.path.basename(file).replace(".txt", "")
            # 给每个数据集名称加文件前缀，避免覆盖
            new_file_data = {}
            for ds_name, ds_info in file_data.items():
                new_ds_name = f"{file_prefix}_{ds_name}"  # 格式：文件名_数据集名
                new_file_data[new_ds_name] = ds_info
            # 合并到总数据集
            all_data.update(new_file_data)
            print(f"✅ 成功解析：{os.path.basename(file)}，包含{len(file_data)}个数据集（命名：{file_prefix}_XXX）")
        except Exception as e:
            print(f"❌ 解析失败：{os.path.basename(file)}，原因：{str(e)}")
    return all_data


def main():
    print("===== D{0-1}KP 动态规划求解系统（批量加载版）=====")

    # 1. 自动加载所有数据文件
    try:
        data = load_all_data_files()
        if not data:
            print("\n❌ 未成功解析到任何数据集，请检查数据文件格式！")
            return
        datasets = get_dataset_list(data)
        print(f"\n🎉 全部解析完成！共识别到 {len(datasets)} 个数据集：")
        for i, name in enumerate(datasets, 1):
            print(f"{i}. {name}")
    except Exception as e:
        print(f"❌ 加载数据失败：{e}")
        return

    # 2. 选择数据集
    while True:
        dataset_choice = input(f"\n请选择数据集（输入序号或名称）：").strip()
        if dataset_choice in datasets:
            dataset_name = dataset_choice
            break
        elif dataset_choice.isdigit() and 1 <= int(dataset_choice) <= len(datasets):
            dataset_name = datasets[int(dataset_choice) - 1]
            break
        else:
            print("输入错误，请重新选择！")

    # 3. 获取数据集详情
    dataset_detail = get_dataset_detail(data, dataset_name)
    cubage = dataset_detail['cubage']
    item_sets = dataset_detail['item_sets']
    N = dataset_detail['N']
    print(f"\n📊 数据集 {dataset_name} 详情：")
    print(f"- 项集数：{N}")
    print(f"- 背包容量：{cubage}")

    # 4. 功能菜单（和之前保持一致）
    while True:
        print("\n===== 功能菜单 =====")
        print("1. 绘制重量-价值散点图")
        print("2. 按第三项价值重量比排序")
        print("3. 求解最优解")
        print("4. 退出")

        choice = input("请选择功能（1-4）：").strip()
        if choice == '1':
            draw_scatter_plot(dataset_name, item_sets)
        elif choice == '2':
            sorted_sets = sort_item_sets_by_ratio(item_sets)
            print("\n前10个项集第三项价值重量比（非递增）：")
            for i in range(min(10, N)):
                v3, w3 = sorted_sets[i][2][0], sorted_sets[i][2][1]
                ratio = v3 / (w3 + 1e-6)
                print(f"项集{i + 1}：价值={v3}，重量={w3}，比例={ratio:.4f}")
        elif choice == '3':
            print("\n🔍 正在求解最优解...")
            result = dynamic_programming_solve(cubage, item_sets)
            print(f"✅ 求解完成！")
            print(f"- 最优总价值：{result['optimal_value']}")
            print(f"- 最优总重量：{result['optimal_weight']}")
            print(f"- 求解耗时：{result['solve_time']}秒")

            save_choice = input("\n是否保存结果？（1=TXT 2=Excel 0=不保存）：").strip()
            if save_choice == '1':
                save_path = input("请输入TXT保存路径（如：./result.txt）：").strip()
                save_result_to_txt(result, dataset_name, cubage, save_path)
                print(f"💾 结果已保存到：{save_path}")
            elif save_choice == '2':
                save_path = input("请输入Excel保存路径（如：./result.xlsx）：").strip()
                export_result_to_excel(result, dataset_name, cubage, item_sets, save_path)
                print(f"💾 结果已导出到：{save_path}")
        elif choice == '4':
            print("👋 退出程序！")
            break
        else:
            print("❌ 输入错误，请选择1-4！")


if __name__ == "__main__":
    main()
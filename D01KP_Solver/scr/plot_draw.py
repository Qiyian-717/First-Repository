import matplotlib.pyplot as plt


def draw_scatter_plot(dataset_name, item_sets):
    """
    绘制重量-价值散点图
    :param dataset_name: 数据集名称（用于标题）
    :param item_sets: 项集列表
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
    plt.rcParams['axes.unicode_minus'] = False

    # 提取所有物品的重量和价值
    weights = []
    values = []
    colors = ['red', 'blue', 'green']
    labels = ['项集-物品0', '项集-物品1', '项集-物品2']

    for idx, item_set in enumerate(item_sets):
        for i in range(3):
            w, v = item_set[i][1], item_set[i][0]
            weights.append(w)
            values.append(v)

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    for i in range(3):
        plt.scatter(weights[i::3], values[i::3], c=colors[i], label=labels[i], alpha=0.6)

    plt.xlabel('物品重量', fontsize=12)
    plt.ylabel('物品价值', fontsize=12)
    plt.title(f'{dataset_name} 重量-价值散点图', fontsize=14)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
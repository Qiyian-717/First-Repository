import re


def parse_d01kp_file(file_path):
    """
    解析D{0-1}KP数据文件（超宽松适配：兼容任意分隔符、关键字大小写、表达式/小数点）
    :param file_path: 数据文件路径
    :return: 字典，格式：{数据集名: {'cubage': 背包容量, 'item_sets': 项集列表, 'N': 项集数}}
    """
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取全部内容，替换所有空白字符（换行/空格/制表符）为单个空格，方便正则匹配
            content = re.sub(r'\s+', ' ', f.read().strip())

            # 正则匹配所有数据集块（匹配规则：任意字符+dimension+任意字符，直到下一个dimension或文件结束）
            dataset_blocks = re.split(r'(?=dimension)', content, flags=re.IGNORECASE)
            for idx, block in enumerate(dataset_blocks):
                block = block.strip()
                if not block:
                    continue

                # ===== 1. 提取数据集名称（优先取块开头的非关键字字符串，无则用IDKP+序号）=====
                dataset_name = f"IDKP{idx + 1}"  # 默认名称
                # 尝试从块开头提取名称（匹配第一个冒号/等号前的字符串）
                name_match = re.match(r'^([^:=]+)', block)
                if name_match and name_match.group(1).strip() and not any(
                        key in name_match.group(1).lower() for key in ['dimension', 'cubage', 'profit', 'weight']):
                    dataset_name = name_match.group(1).strip()

                # ===== 2. 解析维度d（兼容：d=600、d=3*200、dimension=600. 等）=====
                d = None
                d_match = re.search(r'd[=:]\s*([\d\*\.]+)', block, flags=re.IGNORECASE)
                if d_match:
                    d_str = d_match.group(1).strip()
                    if '*' in d_str:
                        parts = d_str.split('*')
                        d = int(float(parts[0].strip())) * int(float(parts[1].strip()))
                    else:
                        d = int(float(d_str))

                # ===== 3. 解析背包容量cubage（兼容：cubage=xxx、capacity=xxx 等）=====
                cubage = None
                cubage_match = re.search(r'(cubage|capacity)\s+of\s+knapsack\s+is\s*([\d\.]+)|cubage[=:]\s*([\d\.]+)',
                                         block, flags=re.IGNORECASE)
                if cubage_match:
                    cubage_str = cubage_match.group(2) if cubage_match.group(2) else cubage_match.group(3)
                    if cubage_str:
                        cubage = int(float(cubage_str.strip()))

                # ===== 4. 解析物品价值profits（兼容：profit of items are: 1,2,3 等）=====
                profits = []
                profit_match = re.search(r'profit\s+of\s+it?ems?\s+are[:=]\s*([\d,\. ]+)', block, flags=re.IGNORECASE)
                if profit_match:
                    profit_str = profit_match.group(1).strip()
                    profits = [int(float(x.strip())) for x in profit_str.split(',') if x.strip()]

                # ===== 5. 解析物品重量weights =====
                weights = []
                weight_match = re.search(r'weight\s+of\s+items?\s+are[:=]\s*([\d,\. ]+)', block, flags=re.IGNORECASE)
                if weight_match:
                    weight_str = weight_match.group(1).strip()
                    weights = [int(float(x.strip())) for x in weight_str.split(',') if x.strip()]

                # ===== 6. 验证并生成项集 =====
                if d and cubage and len(profits) == d and len(weights) == d:
                    N = d // 3
                    item_sets = []
                    for i in range(N):
                        item0 = (profits[3 * i], weights[3 * i])
                        item1 = (profits[3 * i + 1], weights[3 * i + 1])
                        item2 = (profits[3 * i + 2], weights[3 * i + 2])
                        item_sets.append([item0, item1, item2])

                    data[dataset_name] = {
                        'cubage': cubage,
                        'item_sets': item_sets,
                        'N': N
                    }

        return data
    except Exception as e:
        raise Exception(f"数据解析失败：{str(e)}")


def get_dataset_list(data):
    """获取所有数据集名称列表"""
    return list(data.keys()) if data else []


def get_dataset_detail(data, dataset_name):
    """获取指定数据集的详细信息"""
    if dataset_name not in data:
        raise ValueError(f"数据集{dataset_name}不存在")
    return data[dataset_name]
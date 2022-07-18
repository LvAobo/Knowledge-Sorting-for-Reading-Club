import math
import matplotlib
from matplotlib_venn import venn3


# 字体优先级设置
matplotlib.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['axes.unicode_minus'] = False


# 输入变量数并生成存储数组
number_of_variable = int(input("How many variables? :\n"))
variable = [[] for number1 in range(0, number_of_variable)]
variable_input = [[] for number2 in range(0, number_of_variable)]


# 输入变量
def get_variables():
    variables_input = input(f"The variables is (In the form of X1,X1,X1;X2,X2,X2): \n")
    variable_input = variables_input.split(";")
    for number in range(0, number_of_variable):
        variable[number] = variable_input[number].split(",")


# 检验输入是否正确
def test_variables():
    for number in range(0, number_of_variable):
        if len(variable[number]) != len(variable[0]):
            print("The input is wrong! Input again:")
            return -1
    return 1


# 计算信息熵
def calculate_info_entropy(variable, number_of_variable):
    info_entropy = [0 for number in range(0, number_of_variable)]
    info_entropy_cal = [{} for number in range(0, number_of_variable)]

    # 逐一计算各变量
    for number in range(0, number_of_variable):

        # 统计各取值的个数
        for each in range(0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

        # 开始计算
        for each in range(0, len(variable[number])):
            info_entropy[number] -= math.log(info_entropy_cal[number][variable[number][each]]/len(variable[number]),2) / len(variable[number])
        if 1 - info_entropy[number] < 0.0000001 and info_entropy[number] - 1 < 0.0000001:
            info_entropy[number] = 1

    return info_entropy


# 计算两变量联合熵
def calculate_joint_entropy(variable, number_of_variable):
    info_entropy = {}

    # 逐一计算各两变量组合
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):

            # 生成目标变量
            conditional_variable = ["" for number in range(0, len(variable[number1]))]
            for each in range(0, len(conditional_variable)):
                conditional_variable[each] = str(variable[number1][each]) + str(variable[number2][each])
            info_entropy_cal = {}

            # 统计各取值的个数
            for each in range(0, len(conditional_variable)):
                if conditional_variable[each] in info_entropy_cal:
                    info_entropy_cal[conditional_variable[each]] += 1
                else:
                    info_entropy_cal[conditional_variable[each]] = 1

            # 开始计算
            info_entropy[str(number1) + str(number2)] = 0
            for each in range(0, len(conditional_variable)):
                info_entropy[str(number1) + str(number2)] -= \
                    math.log(info_entropy_cal[conditional_variable[each]] / len(conditional_variable), 2) / \
                    len(conditional_variable)

# 计算多变量联合熵
    conditional_variable = ["" for number in range(0, len(variable[0]))]
    for each in range(0, len(conditional_variable)):
        for number in range(0, number_of_variable):
            conditional_variable[each] += str(variable[number][each])

    # 统计各取值的个数
    info_entropy_cal3 = {}
    for each in range(0, len(conditional_variable)):
        if conditional_variable[each] in info_entropy_cal3:
            info_entropy_cal3[conditional_variable[each]] += 1
        else:
            info_entropy_cal3[conditional_variable[each]] = 1

    # 开始计算
    name_all = ""
    for number in range(0, number_of_variable):
        name_all += str(number)
    info_entropy[name_all] = 0
    for each in range(0, len(conditional_variable)):
        info_entropy[name_all] -= math.log(
            info_entropy_cal3[conditional_variable[each]] / len(conditional_variable),
            2) / len(conditional_variable)

    return info_entropy


# 计算互信息
def calculate_mutual_info(variable, number_of_variable):
    info_entropy_cal = [{} for number in range(0, number_of_variable)]

    # 计算各变量频数
    for number in range(0, number_of_variable):
        for each in range (0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

    # 计算每对变量的互信息
    mutual_infor = {}
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1,number_of_variable):

            # 计算这对变量的频数
            combi_prob = {}
            for each in range(0,len(variable[number1])):
                if str(variable[number1][each]) + str(variable[number2][each]) in combi_prob:
                    combi_prob[str(variable[number1][each]) + str(variable[number2][each])] += 1
                else:
                    combi_prob[str(variable[number1][each]) + str(variable[number2][each])] = 1

            # 开始计算互信息
            mutual_infor[str(number1) + str(number2)] = 0
            for each in range(0, len(variable[number1])):
                pn1 = info_entropy_cal[number1][variable[number1][each]] / len(variable[number1])
                pn2 = info_entropy_cal[number2][variable[number2][each]] / len(variable[number2])
                pn1n2 = combi_prob[str(variable[number1][each]) + str(variable[number2][each])] / len(variable[number1])
                k = pn1n2 / (pn1 * pn2)
                mutual_infor[str(number1) + str(number2)] += math.log(k, 2) / len(variable[number1])

    return mutual_infor


# 计算X|X条件信息
def calculate_conditional_info(variable, number_of_variable):
    info_entropy_cal = [{} for number in range(0, number_of_variable)]
    condition_info = {}

    # 计算各变量频数
    for number in range(0, number_of_variable):
        for each in range(0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

    # 开始计算条件信息
    for number1 in range(0, number_of_variable):
        for number2 in range(0, number_of_variable):
            condition_info[str(number1) + str(number2)] = 0
            condition = [0 for number in range(0, len(variable[number1]))]
            for key in info_entropy_cal[number1]:
                p2 = {}
                for each in range(0, len(variable[number1])):
                    if variable[number1][each] == key:
                        if variable[number2][each] in p2:
                            p2[variable[number2][each]] += 1
                        else:
                            p2[variable[number2][each]] = 1
                for each in range(0, len(variable[number1])):
                    if variable[number1][each] == key:
                        condition[each] = p2[variable[number2][each]] / int(info_entropy_cal[number1][key])

            # 计算条件熵
            for each in range(0, len(variable[number1])):
                condition_info[str(number1) + str(number2)] -= math.log(condition[each], 2) / len(variable[number1])

    return condition_info


# 计算X|XX的条件熵
def calculate_12_conditional_info(variable, number_of_variable):
    info_entropy_cal = [{} for number in range(0, number_of_variable)]
    condition_info = {}

    # 计算各变量频数
    for number in range(0, number_of_variable):
        for each in range(0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

    # 开始计算x|xx条件信息
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):

            # 生成条件变量
            conditional_variable = ["" for number in range(0, len(variable[number1]))]
            for each in range(0, len(conditional_variable)):
                conditional_variable[each] = str(variable[number1][each])+str(variable[number2][each])  # 条件变量

            # 计算条件变量分布
            conditional_variable_p = {}
            for each in range(0, len(conditional_variable)):
                if conditional_variable[each] in conditional_variable_p:
                    conditional_variable_p[conditional_variable[each]] += 1
                else:
                    conditional_variable_p[conditional_variable[each]] = 1

            # 找目标变量
            for number3 in range(0, number_of_variable):
                condition_info[str(number3) + str(number1) + str(number2)] = 0
                condition = [0 for number in range(0, len(conditional_variable))]
                for key in conditional_variable_p:
                    p3 = {}
                    for each in range(0, len(conditional_variable)):
                        if conditional_variable[each] == key:
                            if variable[number3][each] in p3:
                                p3[variable[number3][each]] += 1
                            else:
                                p3[variable[number3][each]] = 1
                    for each in range(0, len(conditional_variable)):
                        if conditional_variable[each] == key:
                            condition[each] = p3[variable[number3][each]] / int(conditional_variable_p[key])

                # 计算条件熵
                for each in range(0, len(conditional_variable)):
                    condition_info[str(number3) + str(number1) + str(number2)] -= \
                        math.log(condition[each], 2) / len(conditional_variable)

    return condition_info


# 计算XX|X的条件熵
def calculate_21_conditional_info(variable, number_of_variable):
    info_entropy_cal = [{} for number in range(0, number_of_variable)]
    condition_info = {}

    # 计算各变量频数
    for number in range(0, number_of_variable):
        for each in range(0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

    # 开始计算xx|x条件信息
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):

            # 生成目标变量
            conditional_variable = ["" for number in range(0, len(variable[number1]))]
            for each in range(0, len(conditional_variable)):
                conditional_variable[each] = str(variable[number1][each])+str(variable[number2][each])  # 条件变量

            # 找条件变量
            for number3 in range(0, number_of_variable):
                condition_info[str(number1) + str(number2) + str(number3)] = 0
                condition = [0 for number in range(0, len(conditional_variable))]
                for key in info_entropy_cal[number3]:
                    p3 = {}
                    for each in range(0, len(conditional_variable)):
                        if variable[number3][each] == key:
                            if conditional_variable[each] in p3:
                                p3[conditional_variable[each]] += 1
                            else:
                                p3[conditional_variable[each]] = 1
                    for each in range(0, len(conditional_variable)):
                        if variable[number3][each] == key:
                            condition[each] = p3[conditional_variable[each]] / int(info_entropy_cal[number3][key])

                # 计算条件熵
                for each in range(0, len(conditional_variable)):
                    condition_info[str(number1) + str(number2) + str(number3)] -= \
                        math.log(condition[each], 2) / len(conditional_variable)

    return condition_info


# 冗余信息减协同信息
def calculate_redundancy_minus_synergy(info_entropy, joint_entropy, mutual_info, number_of_variable):
    name_all = ""
    for number in range(0, number_of_variable):
        name_all += str(number)
    return_value = joint_entropy[name_all]
    for number in range(0, number_of_variable):
        return_value -= info_entropy[number]
    for number1 in range(0, number_of_variable):
        for number2 in range(number1+1, number_of_variable):
            return_value += mutual_info[str(number1) + str(number2)]

    return return_value


# 系统规则信息
def calculate_system_rule_information(info_entropy, joint_entropy, number_of_variable):
    name_all = ""
    for number in range(0, number_of_variable):
        name_all += str(number)
    return_value = - joint_entropy[name_all]
    for number in range(0, number_of_variable):
        return_value += info_entropy[number]

    return return_value


# 输出函数
def print_entropy(number_of_variable, info_entropy, joint_entropy, mutual_info, conditional_info,
                  multi_conditional_info, conditional_multi_info, redundancy_minus_synergy, system_rule_information):
    print("=====模块1：各类信息熵计算=====")
    for number in range(0, number_of_variable):
        print(f"H(X{number + 1}) = {round(info_entropy[number],3)}")
    print()
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):
            print(f"H(X{number1 + 1},X{number2 +1}) = {round(joint_entropy[str(number1) + str(number2)], 3)}")
    name_all = ""
    for number in range(0, number_of_variable):
        name_all += str(number)
    print(f"H(all X) = {round(joint_entropy[name_all], 3)}")
    print()
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):
            print(f"I(X{number1 + 1},X{number2 + 1}) = {round(mutual_info[str(number1) + str(number2)],3)}")
    print()
    for number1 in range(0, number_of_variable):
        for number2 in range(0, number_of_variable):
            if number1 != number2:
                print(f"H(X{number2 + 1}|X{number1 + 1}) = {round(conditional_info[str(number1) + str(number2)],3)}")
    print()
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):
            for number3 in range(0, number_of_variable):
                if number3 != number1 and number3 != number2:
                    print(f"H(X{number3 + 1}|X{number1 + 1},X{number2 + 1}) = "
                          f"{round(multi_conditional_info[str(number3) + str(number1) + str(number2)],3)}")
    print()
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):
            for number3 in range(0, number_of_variable):
                if number3 != number1 and number3 != number2:
                    print(f"H(X{number1 + 1},X{number2 + 1}|X{number3 + 1}) = "
                          f"{round(conditional_multi_info[ str(number1) + str(number2) + str(number3)],3)}")
    print()

    print(f"系统规则信息 = {round(system_rule_information,3)}")
    print(f"“系统规则信息”顾名思义，指规则带来的信息多少，既了解到变量间规则信息后，为预测整个系统状态所需信息的减少量。")
    print(f"在三变量系统内也可以这样理解：系统规则信息 = Σ固有信息 + 2*冗余信息 + 协同信息 = Σ互信息 - min互信息 + 协同信息\n")

    print("**** 以下计算目前仅适用于2或3变量系统，4变量及以上系统的计算还在开发中 ****")
    print(f"冗余信息-协同信息 = {round(redundancy_minus_synergy,3)}")
    redundancy_info = info_entropy[0]
    for number1 in range(0, number_of_variable):
        for number2 in range(number1 + 1, number_of_variable):
            if redundancy_info > mutual_info[str(number1) + str(number2)]:
                redundancy_info = mutual_info[str(number1) + str(number2)]
    print(f"冗余信息 = {round(redundancy_info,3)}")
    print(f"协同信息 = {round(redundancy_info - redundancy_minus_synergy,3)}")
    return redundancy_info


# 绘制维恩图
def draw_info(number_of_variable, info_entropy, redundancy_info, redundancy_minus_synergy, mutual_info, multi_conditional_info):
    # 目前只能画三个变量的
    if number_of_variable != 3:
        print("****** 目前版本只能绘制三变量维恩图，抱歉 ******")
    else:
        synergy = redundancy_info - redundancy_minus_synergy
        subset = {'100': multi_conditional_info['012'] + synergy, '110': mutual_info['01'] - redundancy_info,
                  '101': mutual_info['02'] - redundancy_info, '111': redundancy_info, '010': multi_conditional_info['102'] + synergy,
                  '011': mutual_info['12'] - redundancy_info, '001': multi_conditional_info['201'] + synergy}
        my_dpi = 100
        matplotlib.pyplot.figure(figsize=(1000 / my_dpi, 1000 / my_dpi), dpi=my_dpi)
        g = venn3(subsets=subset, set_labels=('X1', 'X2', 'X3'),
                  set_colors=("r", "g", "b"),  # 设置圈的颜色，中间颜色不能修改
                  alpha=0.4,  # 透明度
                  normalize_to=1.0,  # venn图占据figure的比例，1.0为占满
                  )  # 默认数据绘制venn图，只需传入绘图数据

        matplotlib.pyplot.title('系统信息分解图')

        # 修改每个组分的文本
        if subset["100"] != 0:
            g.get_label_by_id('100').set_text(f'H(1|2,3) + S(1,2,3)\n\n= {round(subset["100"], 2)}')
        if subset["010"] != 0:
            g.get_label_by_id('010').set_text(f'H(2|1,3) + S(1,2,3)\n\n= {round(subset["010"], 2)}')
        if subset["001"] != 0:
            g.get_label_by_id('001').set_text(f'H(3|1,2) + S(1,2,3)\n\n= {round(subset["001"], 2)}')
        if subset["110"] != 0:
            g.get_label_by_id('110').set_text(f'S(1,2)\n= {round(subset["110"], 2)}')
        if subset["101"] != 0:
            g.get_label_by_id('101').set_text(f'S(1,3)\n= {round(subset["101"], 2)}')
        if subset["011"] != 0:
            g.get_label_by_id('011').set_text(f'S(2,3)\n= {round(subset["011"], 2)}')
        if subset["111"] != 0:
            g.get_label_by_id('111').set_text(f'I(min)\n= {round(subset["111"], 2)}')

        matplotlib.pyplot.annotate(
            f'H(X1|X2,X3) = {round(multi_conditional_info["012"], 2)}\nS(X1,X2,X3) = {round(synergy, 2)}\n'
            f'H(X1) = {round(info_entropy[0], 2)}',
            color='#000000',
            xy=g.get_label_by_id('100').get_position(),
            xytext=(-140, 40),
            ha='center', textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#ffffff', alpha=0.6),  # 注释文字底纹
            arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3,rad=0.5', color='#000000')  # 箭头属性设置
            )

        matplotlib.pyplot.annotate(
            f'H(X1|X2,X3) = {round(multi_conditional_info["102"], 2)}\nS(X1,X2,X3) = {round(synergy, 2)}\n'
            f'H(X2) = {round(info_entropy[1], 2)}',
            color='#000000',
            xy=g.get_label_by_id('010').get_position(),
            xytext=(140, 40),
            ha='center', textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#ffffff', alpha=0.6),  # 注释文字底纹
            arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3,rad=0.5', color='#000000')  # 箭头属性设置
            )

        matplotlib.pyplot.annotate(
            f'H(X1|X2,X3) = {round(multi_conditional_info["201"], 2)}\nS(X1,X2,X3) = {round(synergy, 2)}\n'
            f'H(X3) = {round(info_entropy[2], 2)}',
            color='#000000',
            xy=g.get_label_by_id('001').get_position(),
            xytext=(-140, -120),
            ha='center', textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#ffffff', alpha=0.6),  # 注释文字底纹
            arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3,rad=0.5', color='#000000')  # 箭头属性设置
            )

        matplotlib.pyplot.show()


def coarsening(number_of_variable):
    result = [[] for i in range(0, 2 ** number_of_variable - number_of_variable - 1)]
    variables = [n for n in range(1, number_of_variable + 1)]
    # print(variables)
    count = 0
    for i in range(2 ** number_of_variable):  # 子集个数，每循环一次一个子集
        combo = []
        for j in range(number_of_variable):  # 用来判断二进制下标为j的位置数是否为1
            if (i >> j) % 2:
                combo.append(variables[j])
        # print(combo)
        if len(combo) >= 2:
            result[count] = combo
            count += 1
    # print(f"hi{result}")
    return result


# 计算X|nX的条件熵
def calculate_1n_conditional_info(variable, number_of_variable):
    info_entropy_cal = [{} for number in range(0, number_of_variable)]
    condition_info = [0 for number in range(0, number_of_variable)]

    # 计算各变量频数
    for number in range(0, number_of_variable):
        for each in range(0, len(variable[number])):
            if variable[number][each] in info_entropy_cal[number]:
                info_entropy_cal[number][variable[number][each]] += 1
            else:
                info_entropy_cal[number][variable[number][each]] = 1

    # 开始计算x|nx条件信息
    for number1 in range(0, number_of_variable):# 目标变量

        # 生成条件变量（其余变量）
        conditional_variable = ["" for number in range(0, len(variable[number1]))]
        for number in range(0, number1):
            for each in range(0, len(variable[number1])):
                conditional_variable[each] += str(variable[number][each])  # 条件变量

        for number in range(number1 + 1, number_of_variable):
            for each in range(0, len(variable[number1])):
                conditional_variable[each] += str(variable[number][each])  # 条件变量
        # print(f"{number1}'s conditional_variable is {conditional_variable}")

        # 计算条件变量分布
        conditional_variable_p = {}
        for each in range(0, len(conditional_variable)):
            if conditional_variable[each] in conditional_variable_p:
                conditional_variable_p[conditional_variable[each]] += 1
            else:
                conditional_variable_p[conditional_variable[each]] = 1

        condition = [0 for number in range(0, len(conditional_variable))]

        for key in conditional_variable_p:
            p3 = {}
            for each in range(0, len(conditional_variable)):
                if conditional_variable[each] == key:
                    if variable[number1][each] in p3:
                        p3[variable[number1][each]] += 1
                    else:
                        p3[variable[number1][each]] = 1

            for each in range(0, len(conditional_variable)):
                if conditional_variable[each] == key:
                    condition[each] = p3[variable[number1][each]] / int(conditional_variable_p[key])
        # print(f"{number1}'s condition is {condition}")
        # 计算条件熵
        for each in range(0, len(conditional_variable)):
            condition_info[number1] -= \
                math.log(condition[each], 2) / len(conditional_variable)

    return condition_info


# 判断是否存在涌现
def is_there_any_emergence(variable, number_of_variable):
    condition_info = calculate_1n_conditional_info(variable, number_of_variable)
    for n in range(0, len(condition_info)):
        if condition_info[n] > 0:
            return -1
    return 1


# 计算涌现信息量
def calculate_emergent_entropy(info_entropy, variable, number_of_variable):
    return_value = 0
    # 计算总联合熵
    conditional_variable = ["" for number in range(0, len(variable[0]))]
    for each in range(0, len(conditional_variable)):
        for number in range(0, number_of_variable):
            conditional_variable[each] += str(variable[number][each])
    info_entropy_cal3 = {}
    for each in range(0, len(conditional_variable)):
        if conditional_variable[each] in info_entropy_cal3:
            info_entropy_cal3[conditional_variable[each]] += 1
        else:
            info_entropy_cal3[conditional_variable[each]] = 1
    joint_entropy = 0
    for each in range(0, len(conditional_variable)):
        joint_entropy -= math.log(
            info_entropy_cal3[conditional_variable[each]] / len(conditional_variable),
            2) / len(conditional_variable)

    # 计算涌现熵
    return_value -= joint_entropy
    for number in range(0, number_of_variable):
        return_value += info_entropy[number]
    return return_value


# *** 以下为主函数 ***
# 不需要的模块可以注释掉，避免计算时间过长

# 模块0：获取变量，不可以注释掉
while True:
    get_variables()
    if test_variables() == 1:
        break


# 模块1：各类信息熵计算
# 信息熵
info_entropy = calculate_info_entropy(variable, number_of_variable)
# 联合熵
joint_entropy = calculate_joint_entropy(variable, number_of_variable)
# 互信息
mutual_info = calculate_mutual_info(variable, number_of_variable)
# 条件信息
conditional_info = calculate_conditional_info(variable, number_of_variable)
# X|XX条件信息
multi_conditional_info = calculate_12_conditional_info(variable, number_of_variable)
# XX|X条件信息
conditional_multi_info = calculate_21_conditional_info(variable, number_of_variable)
# 冗余信息-协同信息
redundancy_minus_synergy = calculate_redundancy_minus_synergy(info_entropy, joint_entropy, mutual_info,
                                                              number_of_variable)
# 系统规则信息
system_rule_information = calculate_system_rule_information(info_entropy, joint_entropy, number_of_variable)
# 输出函数
redundancy_info = print_entropy(number_of_variable, info_entropy, joint_entropy, mutual_info, conditional_info,
                                multi_conditional_info, conditional_multi_info, redundancy_minus_synergy,
                                system_rule_information)


# 模块2：多尺度自动建模
print("\n\n=======模块2：多尺度自动建模=======\n")
is_there_a_emergence = 0
emergent_coarse_set = [[] for i in range(0, 2 ** number_of_variable)]
count = 0
# 遍历所有粗粒化方式
coarse_set = coarsening(number_of_variable)
# 检查每一个粗粒化集合是否满足条件：外部信息O = 0
for throughout in range(0, len(coarse_set)):
    potential_emergence = [[0 for j in range(len(variable[0]))] for i in range(0, len(coarse_set[throughout]))]
    for number in range(0, len(coarse_set[throughout])):
        potential_emergence[number] = variable[coarse_set[throughout][number] - 1]
    yes = is_there_any_emergence(potential_emergence, len(coarse_set[throughout]))
    if yes == 1:  # 存在一级涌现
        is_there_a_emergence = 1
        info_entro = calculate_info_entropy(potential_emergence, len(coarse_set[throughout]))
        emergent_entropy = calculate_emergent_entropy(info_entro, potential_emergence, len(coarse_set[throughout]))
        print(f"X{coarse_set[throughout]}粗粒化方式存在涌现，该涌现信息量为{round(emergent_entropy, 2)}\n")
        emergent_coarse_set[count] = coarse_set[throughout]
        count += 1

# 判断多层涌现
is_there_multy_emergence = 0
emergent_set = [[] for i in range(0, count)]
for number in range(0, count):  # 精简下存涌现粗粒化的数组
    emergent_set[number] = emergent_coarse_set[number]

for set1 in range(0,len(emergent_set) - 1):
    for set2 in range(set1 + 1,len(emergent_set)):
        second_layer = emergent_set[set1] + emergent_set[set2]
        for set in range(0,len(emergent_set)):
            if second_layer == emergent_set[set]:
                is_there_multy_emergence = 1
                print(f"多层涌现： X{emergent_set[set1] } 与 X{emergent_set[set2]}涌现出 X{emergent_set[set]}\n")

if is_there_a_emergence == 0:
    print("该系统内不存在涌现\n")
if is_there_multy_emergence == 0:
    print("该系统内不存在多层涌现\n")


# 模块3：绘制韦恩图
print("\n")
draw_info(number_of_variable, info_entropy, redundancy_info, redundancy_minus_synergy, mutual_info, multi_conditional_info)




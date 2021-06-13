num1 = input("Nhập vào số thứ nhất: ")
num2 = input("Nhập vào số thứ hai: ")


def find_intersection(a, b):
    result = []
    for i in a:
        for j in b:
            if i == j and result.count(i) <= 0:
                result.append(i)

    return result


def find_picking_case(output, num, index, picked, depth):
    clone = picked.copy()
    clone.append(num[index])
    num = num[index + 1:]
    if depth == 0:
        return clone
    for x in range(len(num)):
        result = find_picking_case(output, num, x, clone, depth - 1)
        if result is not None:
            output.append("".join(result))


def main(num):
    output = []
    for i in range(len(num)):
        for j in range(len(num) - i):
            find_picking_case(output, num, j, [], i)
    return output


inter1 = find_intersection(num1, num2)
inter2 = find_intersection(num2, num1)
case1 = main(inter1)
case2 = main(inter2)
case_intersection = find_intersection(case1, case2)
case_intersection = list(map(lambda x: int(x), case_intersection))
case_intersection.sort()
if len(case_intersection) == 0:
    if len(inter1) > 0:
        inter1 = list(map(lambda x: int(x), inter1))
        inter1.sort()
        print(f"Số chung lớn nhất là: {inter1[-1]}")
    else:
        print("Hai số không có phần chung")
else:
    print(f"Số chung lớn nhất là: {case_intersection[-1]}")

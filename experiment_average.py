avg = 0
i = 0
with open("res.txt", "r") as fp:
    line = fp.readline()
    while line:
        line = fp.readline()
        arr = line.split()
        if arr != []:
            # if the line is the result of the program
            if arr[-1] == "%" and arr[0] != "(random)":
                i += 1
                result = arr[5]  # take the percentage
                print(line)
                avg += float(result)

print("average is {:.2f}".format(avg/i))

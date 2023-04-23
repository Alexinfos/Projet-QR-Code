def read(path):
    f = open(path, "r")
    d = f.read()
    f.close()

    lines = d.split("\n")

    data = []
    if len(lines) > 1:
        for l in lines[1:]:
            lineArray = l.split(',')
            arr = []
            
            for e in lineArray:
                try:
                    d = int(e)
                except ValueError:
                    d = e

                arr.append(d)

            data.append(arr)

    return data

def array_to_dict(array):
    dict = {}
    for e in array:
        dict[e[0]] = e[1:]

    return dict
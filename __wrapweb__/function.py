def concatenation(path_first: str, path_second: str) -> str:
    with open('__out__/out.txt', 'w') as out_file, open(path_first) as file_in1, open(path_second) as file_in2:
        out_file.write(file_in1.read())
        out_file.write(file_in2.read())
    return '__out__/out.txt'

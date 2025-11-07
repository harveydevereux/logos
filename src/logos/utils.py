def indent_length(line: str) -> int:
    if len(line.lstrip()) == 0:
        return 0
    for i, s in enumerate(line):
        if s != " ":
            return i

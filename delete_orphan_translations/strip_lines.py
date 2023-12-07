filename = 'C:/Users/debtr/Downloads/lint.txt'

lines = []
with open(filename, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("game/tl"):
            line_number = int(line.split("line")[1].split()[0])
            lines.append((line_number, line))

sorted_lines = sorted(lines, key=lambda x: x[0], reverse=True)

with open(filename, "w", encoding="utf-8") as file:
    for line in sorted_lines:
        file.write(line[1] + "\n")

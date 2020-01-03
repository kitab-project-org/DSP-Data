import sys
import re
import os


def add_heading_numbers(file, splitter):

    writer = open(file + "_headings-id", 'w', encoding="utf8")
    orig_file = open(file, "r", encoding="utf8")
    orig_text = orig_file.read()
    body = orig_text.split(splitter)
    header = body[0]
    text = body[1]
    print(header)
    print("***")
    # lines = body_text.splitlines()
    sections = re.split("(### \|+)", text)
    # sections = re.split("(### \|+ [\s\S]*)", body_text)
    units = ""

    h1_cnt = 0
    h2_cnt = 0
    h3_cnt = 0
    h4_cnt = 0
    h5_cnt = 0

    # for l in lines:
    for i in range(0, len(sections) - 1):
        # if l.startswith("### |||||"):
        if sections[i].startswith("### |||||"):
            h5_cnt += 1

            hr_nr = ".".join([str(h1_cnt), str(h2_cnt), str(h3_cnt), str(h4_cnt), str(h5_cnt)])
            lines = sections[i + 1].split("\n")
            units = units + sections[i] + lines[0] + " " + hr_nr + "\n" + "\n".join(lines[1:])

        elif sections[i].startswith("### ||||"):
            h4_cnt += 1
            h5_cnt += 0

            hr_nr = ".".join([str(h1_cnt), str(h2_cnt), str(h3_cnt), str(h4_cnt), str(h5_cnt)])
            lines = sections[i + 1].split("\n")
            units = units + sections[i] + lines[0] + " " + hr_nr + "\n" + "\n".join(lines[1:])

        elif sections[i].startswith("### |||"):
            h3_cnt += 1
            h4_cnt += 0
            h5_cnt += 0

            hr_nr = ".".join([str(h1_cnt), str(h2_cnt), str(h3_cnt), str(h4_cnt), str(h5_cnt)])
            lines = sections[i + 1].split("\n")
            units = units + sections[i] + lines[0] + " " + hr_nr + "\n" + "\n".join(lines[1:])

        elif sections[i].startswith("### ||"):
            h2_cnt += 1
            h3_cnt = 0
            h4_cnt = 0
            h5_cnt = 0

            hr_nr = ".".join([str(h1_cnt), str(h2_cnt), str(h3_cnt), str(h4_cnt), str(h5_cnt)])
            lines = sections[i + 1].split("\n")
            units = units + sections[i] + lines[0] + " " + hr_nr + "\n" + "\n".join(lines[1:])

        elif sections[i].startswith("### |"):
            h1_cnt += 1
            h2_cnt = 0
            h3_cnt = 0
            h4_cnt = 0
            h5_cnt = 0

            hr_nr = ".".join([str(h1_cnt), str(h2_cnt), str(h3_cnt), str(h4_cnt), str(h5_cnt)])
            lines = sections[i + 1].split("\n")
            units = units + sections[i] + lines[0] + " " + hr_nr + "\n" + "\n".join(lines[1:])
        else:
            units = units + sections[i]

    writer.write(header + splitter + units)


if __name__ == '__main__':

    txt_file = input("Enter the path to the text: ")
    splitter_s = "#META#Header#End#"

    if len(sys.argv) > 0:
        if not os.path.exists(txt_file):
            print("file does not exists: ", txt_file)
        else:
            add_heading_numbers(txt_file, splitter_s)

    else:
        print("give path to the script...!")


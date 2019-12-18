import csv
import re
import os

splitter = "#META#Header#End#"


def get_tag_positions(file):
    # tmp = file.rsplit("/", 1)
    # fileName = tmp[-1]
    # file_path = tmp[0]
    # print(fileName)
    writer = open(file + "_headings-tags", 'w', encoding="utf8")
    # tags = csv.DictReader(open(tags_file, "r", encoding="utf8"), delimiter="\t")

    orig_file = open(file, "r", encoding="utf8")
    orig_text = orig_file.read()
    body_text = orig_text.split(splitter)[1]
    # lines = body_text.splitlines()
    sections = re.split("(### \|+)", body_text)
    # sections = re.split("### \|+", body_text)
    headings = []

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
            # headings.append({"heading": l, "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt)
            #                                                      + "." + str(h4_cnt) + "." + str(h5_cnt)})
            headings.append({"heading": sections[i + 1], "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt) +
                                                                   "." + str(h4_cnt) + "." + str(h5_cnt)})
        # elif l.startswith("### ||||"):
        elif sections[i].startswith("### ||||"):
            h4_cnt += 1
            h5_cnt += 0
            # headings.append({"heading": l, "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt)
            #                                          + "." + str(h4_cnt) + "." + str(h5_cnt)})
            headings.append({"heading": sections[i + 1], "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt) +
                                                                   "." + str(h4_cnt) + "." + str(h5_cnt)})
        # elif l.startswith("### |||"):
        elif sections[i].startswith("### |||"):
            h3_cnt += 1
            h4_cnt += 0
            h5_cnt += 0
            # headings.append({"heading": l, "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt)
            #                                                      + "." + str(h4_cnt) + "." + str(h5_cnt)})
            headings.append({"heading": sections[i + 1], "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt) +
                                                                   "." + str(h4_cnt) + "." + str(h5_cnt)})
        # elif l.startswith("### ||"):
        elif sections[i].startswith("### ||"):
            h2_cnt += 1
            h3_cnt = 0
            h4_cnt = 0
            h5_cnt = 0
            # headings.append({"heading": l, "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt)
            #                                          + "." + str(h4_cnt) + "." + str(h5_cnt)})
            headings.append({"heading": sections[i + 1], "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt) +
                                                                   "." + str(h4_cnt) + "." + str(h5_cnt)})
        # elif l.startswith("### |"):
        elif sections[i].startswith("### |"):
            h1_cnt += 1
            h2_cnt = 0
            h3_cnt = 0
            h4_cnt = 0
            h5_cnt = 0
            # headings.append({"heading": l, "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt)
            #                                          + "." + str(h4_cnt) + "." + str(h5_cnt)})
            headings.append({"heading": sections[i + 1], "number": str(h1_cnt) + "." + str(h2_cnt) + "." + str(h3_cnt) +
                                                                   "." + str(h4_cnt) + "." + str(h5_cnt)})

    print(len(headings))
    for h in headings:
        # title = h['heading']
        title = h['heading'].split("\n")[0]
        num = h['number']
        # tags = re.findall("@SIR@\w+@[a-zA-Z]+@-@\w+@", title)
        # tags = re.findall("@SIR@\w+@\w+-@\w+@", h['heading'])
        tr_tags = re.findall("@SIR@\w+@\w+@-@tr@", h['heading'])
        # remove tags from the heading line and write to file
        writer.write("\t".join([re.sub("@SIR@\w+@\w+@-@tr@ ", "", title), num, ",".join(set(tr_tags))]))
        # writer.write("\t".join([title, num]))
        writer.write("\n")


get_tag_positions(#"/home/rostam/projs/KITAB/Sira/DSP-Data/Original three texts/0230IbnSacd.TabaqatKubra.Shamela0001686-ara1.inProgress")
    "/home/rostam/projs/KITAB/Sira/DSP-Data/Named entities/Tests Tabari/"
                  "0310Tabari.Tarikh.Shamela0009783-ara1inProgress for DSP.completed_tagged")
                  # "0213IbnHisham.SiraNabawiyya.DISAMBIGUATED_HEADER_TAGS.Shamela0023833-ara1_tagged_newTags")
                  # "/home/rostam/projs/KITAB/Sira/DSP-Data/Original three texts/0310Tabari.Tarikh.Shamela0009783-ara1.inProgress for DSP.completed"
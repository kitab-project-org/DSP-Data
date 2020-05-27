# inserting milestones for splitting texts into chunks of the same size

import re
import os
import math
import sys
from itertools import groupby


# Count the length of a text in Arabic characters
def ar_tok_cnt(text):
    ar_chars = "ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًٌٍَُِّْ٠١٢٣٤٥٦٧٨٩ٮٰٹپچژکگیے۱۲۳۴۵‌‍"
    ar_tok = re.compile("[{}]+".format(ar_chars))  # regex for one Arabic token
    toks = re.findall(ar_tok, text)
    return len(toks)


def milestones(file, length, last_ms_cnt, ms_pattern):
    arRa = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")
    splitter = "#META#Header#End#"

    file_name = re.split("-\w{4}(\.(mARkdown|inProgress|completed))?$", file.split("/")[-1])[0]
    print(file_name)
    if re.search("[A-Z]{1}$", file_name):
        continuous = True
    else:
        continuous = False

    with open(file, "r", encoding="utf8") as f1:
        data = f1.read()

        # splitter test
        if splitter in data:
            data_parts = re.split("\n*#META#Header#End#\n*", data)
            head = data_parts[0]
            # remove the final new line and spaces to avoid having the milestone tag in a new empty line
            text = data_parts[1].rstrip()
            # remove old milestone ids
            text = re.sub(" Milestone300", "", text)
            text = re.sub(ms_pattern, "", text)

            # insert Milestones
            ara_toks_count = ar_toks_cnt(text)
            ms_tag_str_len = len(str(math.floor(ara_toks_count / length)))

            all_toks = re.findall(r"\w+|\W+", text)

            token_count = 0
            ms_count = last_ms_cnt

            new_data = []

            for i in range(0, len(all_toks)):
                if arRa.search(all_toks[i]):
                    token_count += 1
                    # d = d.replace("#", "")
                    # d = d.replace("|", "")
                    # d = re.sub("\d|[A-z]|[@#|$-/:-?{-~!\"^_`\[\]]", " ", d)
                    # d = re.sub(" +", " ", d)
                    # d = re.sub("\n{3,}", "\n", d)
                    # if i == len(all_toks) - 1:
                    #     new_data.append(all_toks[i].rstrip())
                    # else:
                    new_data.append(all_toks[i])

                else:
                    # file_name# d = re.sub("\n{3,}", "\n", d)
                    # if i == len(all_toks) - 1:
                    #     new_data.append(all_toks[i].rstrip())
                    # else:
                    new_data.append(all_toks[i])

                if token_count == length or i == len(all_toks) - 1:
                    ms_count += 1
                    if continuous:
                        milestone = " ms" + file_name[-1] + str(ms_count).zfill(ms_tag_str_len)
                    else:
                        milestone = " ms" + str(ms_count).zfill(ms_tag_str_len)
                    new_data.append(milestone)
                    token_count = 0

            ms_text = "".join(new_data)
            # ms_text = re.sub(" +", " ", ms_text)

            test = re.sub(" ms[A-Z]?\d+", "", ms_text)
            # test = re.sub(" +", " ", test)
            if test == text:
                print("\t\tThe file has not been damaged!")
                # Milestones TEST
                ms = re.findall("ms[A-Z]?\d+", ms_text)
                print("\t\t%d milestones (%d words)" % (len(ms), length))
                ms_text = head.rstrip() + "\n\n" + splitter + "\n\n" + ms_text
                with open(file, "w", encoding="utf8") as f9:
                    f9.write(ms_text)
                return ms_count
            else:
                print("\t\tSomething got messed up...")
                return -1

        else:
            print("The file is missing the splitter!")
            print(file)
            return -1


def groupby_books(name):
    b_id = re.split("-ara1|-per1", name)[0]
    if re.search("[A-Z]{1}$", b_id):
        return b_id[:-1]
    else:
        return b_id


if __name__ == '__main__':
    main_folder = input("Enter the path to the OpenITI folder: ")

    ms_len = 300
    if len(sys.argv) > 0:
        if not os.path.exists(main_folder):
            print("invalid path: ", main_folder)
        else:
            # process all texts in OpenITI
            exclude = (["OpenITI.github.io", "Annotation", "_maintenance", "i.mech"])
            for root, dirs, files in os.walk(main_folder):
                book_files = [f for f in files if
                              re.search("^\d{4}\w+\.\w+\.\w+-\w{4}(\.(mARkdown|inProgress|completed))?$", f)]
                # books = map(lambda x: re.split("-ara1|-per1", x)[0], book_files)
                grouped_books = [list(items) for gr, items in groupby(sorted(book_files), key=lambda name: groupby_books(name))]

                for group in grouped_books:
                    if not all(re.search("[A-Z]$", re.split("-\w{4}", x)[0]) for x in sorted(group)):
                        for g in group:
                            milestones(os.path.join(root, g), ms_len, 0, " ms[A-Z]?\d+")

                    elif any(re.search("[A-Z]$", re.split("-ara1|-per1", x)[0]) for x in sorted(group)):
                        prev_ms_cnt = 0
                        group.sort(key=lambda f: f.split("-")[1])
                        grouped_extensions = [list(items) for gr, items in groupby(group,
                                                                                   key=lambda name: name.split("-")[1])]
                        for sub_g in grouped_extensions:
                            prev_ms_cnt = 0
                            for f in sorted(sub_g):
                                prev_ms_cnt = milestones(os.path.join(root, f), ms_len, prev_ms_cnt, " ms[A-Z]?\d+")

    else:
        print("give the path to the script...!")


print("Done!")


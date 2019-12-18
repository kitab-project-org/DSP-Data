"""
Tags passages of the month in the original sources.
The inputs are passage of month files for each source book and the original book (e.g., Ibn Hisham).
"""

import re
import sys
import os


def deNormalize(text):
    alifs = '[إأٱآا]'
    alifReg = '[إأٱآا]'
    # -------------------------------------
    alifMaqsura = '[يى]'
    alifMaqsuraReg = '[يى]'
    # -------------------------------------
    taMarbutas = 'ة'
    taMarbutasReg = '[هة]'
    # -------------------------------------
    hamzas = '[ؤئء]'
    hamzasReg = '[ؤئءوي]'
    # Applying deNormalization
    text = re.sub(alifs, alifReg, text)
    text = re.sub(alifMaqsura, alifMaqsuraReg, text)
    text = re.sub(taMarbutas, taMarbutasReg, text)
    text = re.sub(hamzas, hamzasReg, text)
    return text


def tag_sira_passages(original_txt, passage_file):
    splitter = "#META#Header#End#"
    with open(passage_file, "r", encoding='utf8') as passage_f:
        passage_data = passage_f.read()
        # ibnIshaq_excerpts = re.split("[^#]\n#", ibnIshaq_data)
        # monthly_excerpts = re.split("### | ", passage_data)  # for Ibn Hisham excerpts
        monthly_excerpts = passage_data.split("### | ")  # for Ibn Hisham excerpts

    with open(original_txt, "r") as orig_f:
        orig_txt = orig_f.read()
        orig_content = orig_txt.split(splitter)
        orig_body = orig_content[1]
        orig_head = orig_content[0]

    not_tagged_excerpts = []
    for month_exc in monthly_excerpts:
        month_exc = month_exc.split("\n\n")
        if len(month_exc) > 1:
            month = month_exc[0].strip()
            print(month)
            print("mon exc: ", month_exc)
            for exc in month_exc[1:]:
                exc = re.sub("\W|\d|[A-z]", " ", exc.strip())
                exc = re.sub(" +", " ", exc).strip()
                # print("true exc:", exc, "X")
                # if exc not in [None, ""]:
                exc = exc.strip()
                exc_list = re.split("[^ٱء-ي]+", exc)
                denorm_exc_list = list(map(deNormalize, list(filter(None, exc_list))))
                denorm_exc_patt = "[^ٱء-ي]+".join(denorm_exc_list)

                # denorm_exc_patt = "^" + denorm_exc_patt + "?"
                if re.search(denorm_exc_patt, orig_body):
                    all = re.findall(denorm_exc_patt, orig_body)
                    # if len(all) > 1:
                    #     print(exc, " - ", len(all))
                    matches = re.finditer(denorm_exc_patt, orig_body)

                    for m in matches:
                        orig_body = orig_body[0:m.span()[0]] + "@" + month + "@EXC@BEG@-@00@ " + orig_body[m.span()[0]:m.span()[1]] \
                                    + " @" + month + "@EXC@END@-@00@" + orig_body[m.span()[1]:]

                else:
                    not_tagged_excerpts.append(exc)

                # return

    with open(original_txt + "_month-passages_tagged", "w", encoding="utf8") as tagged_f:
        tagged_f.write(orig_head + "\n" + splitter + "\n" + orig_body)

    with open(original_txt + "_month-passages_not_tagged", "w", encoding="utf8") as not_tagged_f:
        for e in not_tagged_excerpts:
            not_tagged_f.write(e + "\n\n")


if __name__ == '__main__':

    txt_file = input("Enter the path to the text: ")
    excerpt_file = input("Enter the path to the excerpts file: ")

    if len(sys.argv) > 0:
        if not os.path.exists(txt_file):
            print("invalid path: ", txt_file)
        elif not os.path.exists(excerpt_file):
            print("invalid path: ", excerpt_file)
        else:
            tag_sira_passages(txt_file, excerpt_file)

    else:
        print("give the path to the script...!")


"""
Tags Ibn Ishaq (Sira) passages of Kevin's material in the original sources.
To test we use Ibn Hisham text.
The inputs are Kevin's Ibn Ishaq passages and the original book (e.g., Ibn Hisham).
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


def tag_sira_passages(original_txt, excerpts_file):
    splitter = "#META#Header#End#"
    with open(excerpts_file, "r", encoding='utf8') as ibnIshaq_f:
        ibnIshaq_data = ibnIshaq_f.read()
        # ibnIshaq_excerpts = re.split("[^#]\n#", ibnIshaq_data)
        ibnIshaq_excerpts = re.split("\n\n", ibnIshaq_data)  # for Ibn Hisham excerpts
        # ibnIshaq_excerpts = re.split("\n\n", ibnIshaq_data) # for Tabari excerpts
    print(ibnIshaq_excerpts[23])
    # return

    with open(original_txt, "r") as orig_f:
        orig_txt = orig_f.read()
        orig_content = orig_txt.split(splitter)
        orig_body = orig_content[1]
        orig_head = orig_content[0]

    not_tagged_excerpts = []
    de_arr = []
    matches_positions = []

    for exc in ibnIshaq_excerpts:
        exc = exc.strip()
        if not (exc.startswith("###")):
            exc = re.sub("\W|\d|[A-z]", " ", exc).strip()
            exc = re.sub(" +", " ", exc).strip()
            # print("true exc:", exc, "X")
            if exc not in [None, ""]:
                exc = exc.strip()
                exc_list = re.split("[^ٱء-ي]+", exc)
                denorm_exc_list = list(map(deNormalize, list(filter(None, exc_list))))
                # denorm_exc_list = list(filter(None, exc_list))
                denorm_exc_patt = "[^ٱء-ي]+".join(denorm_exc_list)

                # denorm_exc_patt = "^" + denorm_exc_patt + "?"
                if re.search(denorm_exc_patt, orig_body):
                    all = re.findall(denorm_exc_patt, orig_body)
                    # if len(all) > 1:
                    #     print(exc, " - ", len(all))
                    matches = re.finditer(denorm_exc_patt, orig_body)

                    for m in matches:
                        orig_body = orig_body[0:m.span()[0]] + "\n#~:SIR_IbnIshaq_BEG:\n" + orig_body[m.span()[0]:m.span()[1]] \
                                    + "\n#~:SIR_IbnIshaq_END:\n" + orig_body[m.span()[1]:]
                    # orig_body = re.sub(denorm_exc_patt.strip(), "\n@SIR@EXC@BEG@-@00@ " + exc + " @SIR@EXC@END@-@00@\n", orig_body)

                else:
                    not_tagged_excerpts.append(exc)
    # print(matches_positions)
    # positions_sorted = matches_positions.sort(key=operator.itemgetter(0))
    # print(positions_sorted)
    # for i in range(1, len(positions_sorted)):
    #     if positions_sorted[i][0] < positions_sorted[i - 1][1]:
    #         print(positions_sorted[i])

    with open(original_txt + "_excerpts_tagged", "w", encoding="utf8") as tagged_f:
        tagged_f.write(orig_head + "\n" + splitter + "\n" + orig_body)

    with open(original_txt + "_excerpts_not_tagged", "w", encoding="utf8") as not_tagged_f:
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

import sys
import os
import csv
import re

splitter = "#META#Header#End#"

# normalizeArabicLight(text) - fixing only Alifs, AlifMaqsuras; replacing hamzas on carriers with standalone hamzas
def normalizeArabicLight(text):
    new_text = text
    # patterns to replace
    rep = {"[إأٱآا]": "ا",
           "[يى]ء": "ئ",
           "ى": "ي",
           "ى": "ي",
           "(ؤ)": "ء",
           "(ئ)": "ء"
           }

    # do the replacement
    # rep = dict((k, v) for k, v in rep.items())
    # pattern = re.compile("|".join(rep.keys()))
    for k, v in rep.items():
        new_text = re.sub(k, rep[k], new_text)
    return new_text


def apply_tag(strr, t):
    # normalized_tag = re.sub(" ", "[^ٱء-ي]+", normalizeArabicLight(t['entity'].strip()))
    normalized_tag = re.sub(" ", "[^ٱء-ي]+", t['entity'].strip())
    new_strr = strr
    normalized_strr = normalizeArabicLight(new_strr)
    prefixes = ["ب", "ل", "ك", "و", "ف", ""]
    for p in prefixes:
        # pattern = r"\b" + normalizeArabicLight(p) + normalized_tag + r"\b"
        pattern = r"\b" + p + normalized_tag + r"\b"
        new_strr = re.sub(pattern, "@SIR@" + (t['category']).upper() + t['tag'] + "@-@00@" + " " + p + t['entity'],
                          new_strr)
    return new_strr


def tag_text(file, tags_file):

    writer = open(file + "_tagged", 'w')
    tags = csv.DictReader(open(tags_file, "r", encoding="utf8"), delimiter=",")

    orig_file = open(file, "r", encoding="utf8")
    orig_text = orig_file.read()
    body_text = orig_text.split(splitter)[1]
    missing_tags = []
    for t in tags:
        if t['tag_status'] == "FALSE":
            # body_text = list(map(lambda x: apply_tag(x, t), list(lines2t)))
            body_text = apply_tag(body_text, t)
            if len(re.findall("@SIR@" + (t['category']).upper() + t['tag'] + "@-@00@", body_text)) < 1:
                missing_tags.append(t)
            t['tag_status'] = 'TRUE'

    writer.write("\n".join([orig_text.split(splitter)[0] + splitter + body_text]))

    # write the missing tags to a file
    if len(missing_tags) > 0:
        with open(file + "_missing_tags", 'w') as tag_w:
            missing_tags = csv.DictWriter(tag_w, fieldnames=['entity', 'tag', 'category', 'tag_status'])
            missing_tags.writeheader()
            for t in tags:
                missing_tags.writerow(t)

    # update the tags file
    # tags.seek(0)
    # with open(tags_file + "_updated", 'w') as tag_w:
    #     tag_updated = csv.DictWriter(tag_w, fieldnames=['entity', 'tag', 'category', 'tag_status'])
    #     tag_updated.writeheader()
    #     print("tags len2: ", tags)
    #     for t in tags:
    #         tag_updated.writerow(t)


if __name__ == '__main__':

    txt_file = input("Enter the path to the text: ")
    tag_file = input("Enter the path to the tagset file: ")

    if len(sys.argv) > 0:
        if not os.path.exists(txt_file):
            print("invalid path: ", txt_file)
        elif not os.path.exists(tag_file):
            print("invalid path: ", tag_file)
        else:
            tag_text(txt_file, tag_file)

    else:
        print("give the path to the script...!")

print("Done!")

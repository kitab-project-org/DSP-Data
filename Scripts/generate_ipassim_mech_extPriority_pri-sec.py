"""
Prepares passim input for the whole corpus. Chooses the file extensions according to the following priority:
mARkdown, completed, inProgress, no extension

"""
import re
import os
import sys
from itertools import groupby
import pandas as pd


def roundup(x, par):
    new_x = int(math.ceil(int(x) / float(par)) * par)
    return new_x


def normalize_ara_extra_light(text):
    new_text = text
    # patterns to replace
    rep = {}

    # do the replacement
    for k, v in rep.items():
        new_text = re.sub(k, rep[k], new_text)
    return new_text


def text_cleaner(text):
    text = normalize_ara_extra_light(text)
    text = re.sub("\W|\d|[A-z]", " ", text)
    text = re.sub(" +", " ", text)
    return text


def mechanical_chunking(file_name, body_data, target_path, ms, threshold):
    # file_name = path_full.split("/")[-1]
    file_id = re.sub("\d{4}\w+\.\w+\.", "", file_name)

    target_path = os.path.join(target_path, file_id)
    print("target : ", target_path)
    # run generation
    cex = []

    if os.path.exists(target_path + "-%05d" % thresh):
        cnt = 0
    else:
        # with open(path_full, "r", encoding="utf8") as f1:
        #     data = f1.read()
        #     data = data.split(split_str)[1]
        #     data = re.split(ms, data)
            body_data = re.split("(" + ms + ")", body_data)

            print("\t%d items will be created..." % len(body_data))

            rec = '{"id":"%s", "series":"%s", "text": "%s", "seq": %d}'

            counter = 0

            i = 0
            while i < len(body_data) - 2: # n-th item in data is "" and (n-1)th is the last msID, so we skip them
                counter += 1
                # new_id = file_id + ".ms%s" % str(counter).zfill(ms_cnt_str_len)
                new_id = file_id + "." + body_data[i + 1]
                text = text_cleaner(body_data[i])
                seq = int(re.sub('[^0-9]', "", body_data[i + 1]))
                rec_text = rec % (new_id, file_id, text, seq)

                cex.append(rec_text)

                if counter % threshold == 0:
                    with open(target_path + "-%05d" % counter, "w", encoding="utf8") as ft:
                        ft.write("\n".join(cex))
                    cex = []
                # update the data index to jump to the next data cell since data has data and msIDs
                i += 2

            counter_final = roundup(counter, threshold)
            with open(target_path + "-%05d" % counter_final, "w", encoding="utf8") as ft:
                ft.write("\n".join(cex))

            cnt = 1

    return cnt


def check_pri_ids(full_id, pri_list):
    b_id = full_id.split(".")[2] # get the last part of the name, book id, e.g., JK00001-ara1.inProgress
    id_nr = re.split("-ara1|-per1", b_id)[0] # get the book id, e.g., JK00001 or JK00001A
    if re.search("[A-Z]{1}$", id_nr):
        id_nr = id_nr[:-1]
    if id_nr in pri_list:
        return True
    else:
        return False


# def groupby_books(full_id):
#     id_parts = re.split("-ara1|-per1", full_id)
#     if re.search("[A-Z]{1}$", id_parts[0]):
#         return (id_parts[0][:-1], id_parts[1])
#     else:
#         return (id_parts[0], id_parts[1])


if __name__ == '__main__':

    main_folder = input("Enter the path to the OpenITI folder: ")
    target_folder = input("Enter the path to write the new files: ")
    metadata_file = input("Enter the path to the metadata file: ")
    filter_pri_books = input("Do you want to filter primary books? (y or n) ")

    if len(sys.argv) > 0:
        if not os.path.exists(main_folder):
            print("invalid path: ", main_folder)
        elif not os.path.exists(target_folder):
            print("invalid path: ", target_folder)
        elif not os.path.exists(metadata_file):
            # metadata file is placed in the current folder!
            print("invalid metadata path: ", metadata_file)

        else:
            while filter_pri_books.capitalize() not in ["Y", "N"]:
                filter_pri_books = input("Do you want to filter primary books? (y or n) ")

            print()
            print("Generating mechanical passim corpus...")
            print()

            count = 1
            milestone = "ms[A-Z]?\d+"
            splitter = "#META#Header#End#"
            thresh = 1000

            metadata = pd.read_csv(metadata_file, delimiter="\t")  # ), index_col=1, skiprows=1).T.to_dict()
            pri_metadata = metadata[metadata["status"] == "pri"]
            pri_books = list(pri_metadata['id'])

            for root, dirs, files in os.walk(main_folder):
                dirs[:] = [d for d in dirs]  # if d not in zfunc.exclude]
                texts = [f for f in files if
                         re.search("^\d{4}\w+\.\w+\.\w+-\w{4}(\.(mARkdown|completed|inProgress))?$", f)]
                # texts_noExt = set([re.split("\.(mARkdown|completed|inProgress)", t)[0] for t in texts])

                if filter_pri_books.capitalize() == "Y":
                    pri_texts = list(filter(lambda x: check_pri_ids(x, pri_books), texts))
                    grouped_ids = [list(items) for gr, items in
                               groupby(sorted(pri_texts), key=lambda name: re.split("-ara1|-per1", name)[0])]
                elif filter_pri_books.capitalize() == "N":
                    grouped_ids = [list(items) for gr, items in
                           groupby(sorted(texts), key=lambda name: re.split("-ara1|-per1", name)[0])]

                id_ext_dict = {}
                for g in grouped_ids:
                    g = sorted(g) # when sorted, the first item will be the no-extension file
                    key = g[0].split("-")[0]
                    id_ext_dict[key] = g

                processed_ids = []
                for key, value in id_ext_dict.items():
                    if key not in processed_ids:
                        if re.search("[A-Z]{1}$", key):
                            selected_parts = []
                            multiple_ids = [(k,v) for k,v in id_ext_dict.items() if k[:-1] == key[:-1]]
                            processed_ids.extend([x[0] for x in multiple_ids])
                            for id_ext in multiple_ids:
                                if id_ext[1][0] + ".mARkdown" in id_ext[1]:
                                    selected_parts.append(id_ext[1][0] + ".mARkdown")
                                elif id_ext[1][0] + ".completed" in id_ext[1]:
                                    selected_parts.append(id_ext[1][0] + ".completed")
                                elif id_ext[1][0] + ".inProgress" in id_ext[1]:
                                    selected_parts.append(id_ext[1][0] + ".inProgress")
                                else:
                                    selected_parts.append(id_ext[1][0])

                            # generate a single name from all parts of the books, which have "A", "B", ... at the end.
                            # Here we take one of the names and generate a single name by removing "A", "B", "C", ...
                            txt_id = re.sub("^\d{4}\w+\.\w+\.", "", selected_parts[0])  # get the book id
                            # next two lines are to remove "A", "B", "C", ... from the file names to name the
                            # json files and records for passim inputs
                            txt_name_parts = txt_id.split("-")
                            txt_id = txt_name_parts[0][:-1] + "-" + txt_name_parts[1]
                            tmp_data = []
                            for part in sorted(selected_parts):
                                with open(os.path.join(root, part), "r", encoding="utf8") as f1:
                                    multi_part_data = f1.read()
                                    tmp_data.append(multi_part_data.split(splitter)[1])

                            data = "\n".join(tmp_data)

                            count += mechanical_chunking(txt_id, data, target_folder, milestone, thresh)
                            if count % 100 == 0:
                                print()
                                print("=============" * 2)
                                print("Processed: %d" % count)
                                print("=============" * 2)
                                print()

                        else:
                            no_ext_file = sorted(id_ext_dict[key])[0] # the first one in a sorted list is the no-extension file
                            # print("k: ", no_ext_file)
                            if no_ext_file + ".mARkdown" in id_ext_dict[key]:
                                txt_full_name = no_ext_file + ".mARkdown"
                            elif g[0] + ".completed" in id_ext_dict[key]:
                                txt_full_name = no_ext_file + ".completed"
                            elif g[0] + ".inProgress" in id_ext_dict[key]:
                                txt_full_name = no_ext_file + ".inProgress"
                            else:
                                txt_full_name = no_ext_file

                            with open(os.path.join(root, txt_full_name), "r", encoding="utf8") as f1:
                                data = f1.read()
                                data = data.split(splitter)[1]
                                txt_id = re.sub("^\d{4}\w+\.\w+\.", "", txt_full_name)
                                count += mechanical_chunking(txt_id, data, target_folder, milestone, thresh)
                                if count % 100 == 0:
                                    print()
                                    print("=============" * 2)
                                    print("Processed: %d" % count)
                                    print("=============" * 2)
                                    print()


print("Done!")

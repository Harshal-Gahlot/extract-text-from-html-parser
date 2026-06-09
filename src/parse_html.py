def parse(file: str):
    with open(file, mode="r", encoding="utf-8") as input_f, open(file=file.removesuffix(".html") +" output.txt",mode="w", encoding="utf-8") as out_f:
        position_idx_list = []
        content = input_f.read()
        mainStartIdx = content.find('<main id="content-container">')
        mainEndIdx = content.find('</main>')
        # content is <main>
        content = content[mainStartIdx:mainEndIdx]
        data_as_list = []
        end = 0
        data_as_start_idx = content.find('data-as="') + 12 # since len('data-as="p">') = 12
        # if we didn't find text content .find() will return -1
        while data_as_start_idx != -1:
            data_as_start_idx += end
            end = content[data_as_start_idx:].find("</span>") + data_as_start_idx
            print(data_as_start_idx, end)
            position_idx_list.append([data_as_start_idx, "text"])
            data_as_list.append(
                content[data_as_start_idx: end]
            )
            data_as_start_idx = content[end: ].find('data-as="')

        print(data_as_start_idx, end)
        out_f.write(content.replace("\n", " "))
        for l in data_as_list:
            print(l.replace("\n", "\\n"), end="\n\n")

# cd src and then run:
parse("../Action - Chainlit.html")
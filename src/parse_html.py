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
        data_as_start_idx = content.find('data-as="') # since len('data-as="p">') = 12
        # if we didn't find text content .find() will return -1
        while data_as_start_idx != -1:
            data_as_start_idx += end + 12
            end = content[data_as_start_idx:].find("</span>") + data_as_start_idx
            position_idx_list.append([data_as_start_idx, "text"])
            data_as_list.append(
                content[data_as_start_idx: end]
            )
            data_as_start_idx = content[end: ].find('data-as="')

        filtered_para_list = []

        for para in data_as_list:
            filter_para = ""
            start = 0
            end = para.find("<")
            if end == -1:
                filtered_para_list.append(para)
                continue
            while True:
                filter_para += para[start: end]
                start = para[end:].find(">") + end + 1
                end = para[start:].find("<")
                if end == -1: 
                    break
                end += start
            filter_para += para[start: end]
            filtered_para_list.append(filter_para)
        
        formatted_data_list = []
        # ig we can make it better/faster by doing this above only
        for para in filtered_para_list:
            if "\n" in para:
                whole = ""
                for part in para.split("\n"):
                    whole += part.strip() + " "
                formatted_data_list.append(whole)
            else:
                formatted_data_list.append(para)
        
        code_data_as_list = []
        code_end = 0
        code_data_as_start_idx = content.find('<pre') + 1
        while code_data_as_start_idx != code_end:
            code_end = content[code_data_as_start_idx:].find("</pre") + code_data_as_start_idx
            position_idx_list.append([code_data_as_start_idx, "code"])
            code_data_as_list.append(
                content[code_data_as_start_idx - 1: code_end]
            )
            code_data_as_start_idx = content[code_end: ].find('<pre') + code_end + 1
        
        code_filtered_para_list = []

        for para in code_data_as_list:
            code_filter_para = ""
            start = 0
            end = para.find("<")
            if end == -1:
                code_filtered_para_list.append(para)
                continue
            while True:
                code_filter_para += para[start: end]
                start = para[end:].find(">") + end + 1
                end = para[start:].find("<") 
                if end == -1: 
                    break
                end += start
            code_filter_para += para[start: end]
            code_filtered_para_list.append(code_filter_para)
        
# cd src and then run:
parse("../Action - Chainlit.html")
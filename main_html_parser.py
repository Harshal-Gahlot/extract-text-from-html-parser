from pathlib import Path
import os
# cd src and then run this file:

def filterMainPart(data_list: list, kind: str) -> list:
    """cleaning up the data list and removing all the DOM \\<tag> code
    in between actual text/code content. also formatting text content"""
    result_list = []

    for para in data_list:
        filter_para = ""
        start = 0
        end = para.find("<")
        if end == -1:
            result_list.append(para)
            continue
        while True:
            filter_para += para[start: end]
            start = para[end:].find(">") + end + 1
            end = para[start:].find("<")
            if end == -1: 
                break
            end += start
        filter_para += para[start: end]

        # formatting text kind content only.
        if kind == "text":
            formatted_para = ""
            for part in filter_para.split("\n"):
                formatted_para += part.strip() + " "
            result_list.append(formatted_para)
        # for code kind
        else: result_list.append(filter_para)
        
    return result_list

def parse(file: str):
    position_idx_list = []

    def extractMainPart(startFindUniqueCase: str, endFindUniqueCase: str, startOffset: int, kind: str, content: str) -> list:
        data_list = []
        # start and end are indices, within relevant content exist, probably mixed with DOM code
        end = 0 
        start = content.find(startFindUniqueCase) 
        # if we didn't find text content, .find() will return -1
        while start != -1:
            start += end + startOffset
            end = content[start:].find(endFindUniqueCase) + start
            position_idx_list.append([start, kind])
            data_list.append(
                content[start: end]
            )
            start = content[end: ].find(startFindUniqueCase)
        
        return filterMainPart(data_list, kind)
        
    with open(file, mode="r", encoding="utf-8") as input_f, open(file=file.removesuffix(".html") + " output.txt",mode="w", encoding="utf-8") as out_f:
        content = input_f.read()
        mainStartIdx = content.find('<main id="content-container">')
        mainEndIdx = content.find('</main>')
        content = content[mainStartIdx: mainEndIdx] # content is <main>

        # startOffset = 12 since len('data-as="p">') = 12
        text_data_as_list = extractMainPart('data-as="', "</span>", 12, "text", content)
        
        # startOffset=0 since </pre...>'s len is not constant, we keep </pre and let filterMainPart clean it up.
        code_data_as_list = extractMainPart('<pre', '</pre', 0, "code", content)
        
        text_counter = 0
        code_counter = 0
        final_result_list = []
        position_idx_list.sort()

        for [_, kind] in position_idx_list:
            match kind:
                case "text":
                    final_result_list.append(text_data_as_list[text_counter])
                    text_counter += 1
                case "code":
                    final_result_list.append(code_data_as_list[code_counter])
                    code_counter += 1

        for para in final_result_list:
            out_f.write(para + "\n\n")

def parseAllHtml():
    for f in all_html_files:
        parse(str(f))

def clearTxt():
    """clear all created text files"""
    for f in all_text_files:
        f.unlink()

all_files = Path("./docs")
all_html_files = all_files.glob('*.html')
all_text_files = all_files.glob('*.txt')

parseAllHtml()
# clearTxt()
# parse("./docs/Action - Chainlit.html")
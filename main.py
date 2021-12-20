import argparse
import os
import sys
from glob import glob
import html
from xhtml2pdf import pisa  # import python module

# Lines will be broken if over specified char count
BREAK_LIMIT = 110
output_filename = "out.pdf"
# Define your data
MAIN_TEMPLATE = """
<html>
<style>

body{
font-family:STSong-Light;
}
.code {
border: 1px solid grey;
padding: 1px;
overflow: hide;
font-family:STSong-Light;
}
pre {
font-size:12px;
font-family:STSong-Light;
}
</style>
<body>
<h1>Code Listing</h1>
%%%code%%%
</body>
</html>"""
CODE_TEMPLATE = """
<hr><div>
    <h1>%%%name%%%</h1>
    <div class="code">
        <pre>%%%snippet%%%</pre>
    </div>
</div>"""
# ACCEPTED_EXTENSIONS



def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(
        source_html,  # the HTML to convert
        dest=result_file)  # file handle to recieve result
    result_file.close()  # close output file
    return pisa_status.err


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert files in destination into a pdf')
    parser.add_argument('-dst',
                        help='folder containing your source files',
                        required=True)
    parser.add_argument('-out',
                        help='name of pdf to output',
                        default="out.pdf")
    parser.add_argument('ext',
                        help='list of file extensions to parse',
                        nargs="*")
    args = parser.parse_args()
    if args.dst[-1] != "/": args.dst += "/"
    files_grabbed = []
    for type in args.ext:
        files_grabbed.extend(glob(args.dst + "**/*." + type, recursive=True))

    source_html = MAIN_TEMPLATE
    code_html = ""
    for file in files_grabbed:
        with open(file, 'r',encoding='UTF-8') as f:
            lines = f.readlines()
            contents = ""
            for line in lines:
                if len(line) > BREAK_LIMIT:
                    contents += line[:BREAK_LIMIT] + "\n" + line[BREAK_LIMIT:]
                else:
                    contents += line
            contents = contents.replace("    ", "  ")
            contents = contents.replace("\t", "    ")
            code_html += CODE_TEMPLATE.replace(
                "%%%name%%%",
                file.replace(args.dst, "")).replace("%%%snippet%%%",
                                                    html.escape(contents))
    pisa.showLogging()
    convert_html_to_pdf(source_html.replace("%%%code%%%", code_html), args.out)
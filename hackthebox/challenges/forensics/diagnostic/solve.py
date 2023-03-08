from oletools.olevba import *


def check_for_vba():
    doc = './diagnostic.doc'
    vba_parser = VBA_Parser(doc)
    vba_code = vba_parser.extract_all_macros()
    if vba_code:
        print("Found macros")
        for filename, code in vba_code:
            print(f"Filename: {filename}")

    else:
        print("No macros")

def get_pshell_code():
    s = open('./223_index_style_fancy.html', 'r').read()
    print(s)
    
def main():
    get_pshell_code()

if __name__ == '__main__':
    main()

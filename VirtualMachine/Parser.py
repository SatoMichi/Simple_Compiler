
def parser(code):
    code = re.sub(r"//.*","",code)
    code = code.split(" ")
    result = {"Type":"", "arg1":"", "arg2":""}
    
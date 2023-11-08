#define keyword file object
class KeywordFile:
    def __init__(self, path, type): #define keyword file object using inputs of the filepath to open and the data type ("fixed" or "short")
        match type: #check the given type to determine whether to interpret file via fixed width or via comma separation
            case "fixed":
                with open(path) as f:
                    keyfile_contents=f.read()
                    
            case "short":
                raise ValueError("Short keyfile format not supported yet\n")
            case __:
                raise ValueError("Unknown keyfile type\n")

k=KeywordFile("test_keyword.k","fixed")

import re
def fuzzyfinder(input_str, collection):
    suggestions = []
    pattern = '.*?'.join(input_str)    # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)         # Compiles a regex.
    for item in collection:
        match = regex.search(item)      # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]

def muti_strs_finder(input_str, collection):
    strs = input_str.split()
    input_collection = collection
    output_str_list = []
    for i in range(len(strs)):
        output_str_list = fuzzyfinder(strs[i], input_collection)
        if len(output_str_list) ==0:
            if i==0:
                return output_str_list
        else:
            input_collection = output_str_list
    return input_collection
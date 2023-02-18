import re

pattern = re.compile("[e]")
if pattern.match("Proceed"):
    print("yes")
else:
    print("no")

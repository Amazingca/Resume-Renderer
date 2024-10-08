from datetime import date

configPrototype = {
    "vars": {
        "title": "",
        "isOnline": "",
        "onlineDelimiter": "",
        "delimiter": "",
        "bullet": "",
        "width": ""
    },
    "profile": {
        "name": "",
        "pronouns": "",
        "email": "",
        "phone": ""
    },
    "rows": [
        {
            "title": "",
            "titleRight": "",
            "description": "",
            "descriptionRight": "",
            "body": "",
            "bullets": [
                "",
                ...
            ]
        },
        ...
    ]
}

config = {}

keyPairDataTypes = ["VARIABLES", "PROFILE"]
integerKeywords = ["width"]

def constructData(path):
    with open(path) as data:
        rowType = ""
        newRow = False
        for i, line in enumerate(data):
            line = line[:-1]
            if line[0:4] == "--- ":
                rowType = line.split(" ")[1]
                newRow = True
                continue
            if line[0] == "#":
                continue
            if rowType in keyPairDataTypes:
                if rowType not in config:
                    config[rowType] = {}
                config[rowType][line.split("=")[0]] = line.split("=")[1]
                if line.split("=")[0] in integerKeywords:
                    config[rowType][line.split("=")[0]] = int(line.split("=")[1])
            elif "ROW" in rowType:
                if "ROWS" not in config:
                    config["ROWS"] = []
                isBullet = line.split("=")[0] == "bullets"
                if newRow == True:
                    config["ROWS"].append({
                        "divider": True if rowType == "ROW" else False,
                        line.split("=")[0]: line.split("=")[1] if not isBullet else line.split("=")[1].split(",,")
                    })
                    newRow = False
                else:
                    config["ROWS"][-1][line.split("=")[0]] = line.split("=")[1] if not isBullet else line.split("=")[1].split(",,")

def sectionDivider(divide, f):
    if (divide == True):
        print(config["VARIABLES"]["delimiter"] * config["VARIABLES"]["width"], file=f)
    elif config["VARIABLES"]["adelimiter"] != "":
        print(config["VARIABLES"]["adelimiter"] * config["VARIABLES"]["width"] if config["VARIABLES"]["adelimiter"] != "\\n" else "", file=f)

def formatEmail():
    return config["PROFILE"]["email"].replace("@", config["VARIABLES"]["onlineDelimiter"] if config["VARIABLES"]["isOnline"] == "true" else "@")

def outputHeader(f):
    for key in config["PROFILE"]:
        match key:
            case "name":
                if "email" in config["PROFILE"]:
                    print(f"""{config["PROFILE"][key]}{f"{formatEmail():>{config['VARIABLES']['width'] - len(config['PROFILE'][key])}}"}""", file=f)
                    continue
            case "phone":
                if len(config["PROFILE"]) >= 4 and "pronouns" in config["PROFILE"]:
                    print(f"""{config["PROFILE"]["pronouns"]}{f"{config['PROFILE'][key]:>{config['VARIABLES']['width'] - len(config['PROFILE']['pronouns'])}}"}""", file=f)
            case "pronouns" | "email":
                continue
            case "linkedin" | "github":
                print(f"{config['PROFILE'][key]:>{config['VARIABLES']['width']}}", file=f)
                continue
            case _:
                print(config["PROFILE"][key], file=f)

def outputRows(f):
    for row in config["ROWS"]:
        sectionDivider(row["divider"], f)
        if "title" in row:
            titleRight = row['titleRight'] if 'titleRight' in row else ''
            print(f"""{row["title"].upper()}{f"{titleRight:>{config['VARIABLES']['width'] - len(row['title'])}}"}""", file=f)
        if "subtitle" in row:
            subtitleRight = row['subtitleRight'] if 'subtitleRight' in row else ''
            print(f"""{row["subtitle"]}{f"{subtitleRight:>{config['VARIABLES']['width'] - len(row['subtitle'])}}"}""", file=f)
        if "description" in row:
            descriptionRight = row['descriptionRight'] if 'descriptionRight' in row else ''
            print(f"""{row["description"]}{f"{descriptionRight:>{config['VARIABLES']['width'] - len(row['description'])}}"}""", file=f)
        if "body" in row:
            for line in row["body"].split("\\n"):
                print("\n".join(cropWidth(line, "")), file=f) # Print each newline independant from cutoffs when cropping
        if "bullets" in row:
            for bullet in row["bullets"]:
                print("\n".join(cropWidth(bullet, config['VARIABLES']['bullet'])), file=f)

def cropWidth(line, newLineSpacer):
    if (config["VARIABLES"]["applyWrap"] == "false"):
        return [newLineSpacer + line]
    line = newLineSpacer + line
    lines = []
    while (len(line) > config["VARIABLES"]["width"]): # While we still have line overflow
        indexSelection = config["VARIABLES"]["width"]
        while (line[indexSelection - 1] != " "):
            indexSelection -= 1 # Keep decremementing index until we can crop at a space
        lineSelection = line[:indexSelection]
        lines.append(lineSelection)
        line = (" " * len(newLineSpacer)) + line[indexSelection:] # Add associated spacing, like if we're on bullets
    lines.append(line)
    return lines

if __name__ == "__main__":
    path = input("Enter path for the config file, or nothing for default (\"./config.txt\"): ")
    constructData(path if path != "" else "./config.txt")
    print(f"Creating Resume{': ' if 'title' in config['VARIABLES'] else ''}", end="" if "title" in config["VARIABLES"] else "\n")
    if "title" in config["VARIABLES"]:
        print(config["VARIABLES"]["title"])
    fileName = f"./{config['PROFILE']['name'].split(' ')[0]}{config['PROFILE']['name'].split(' ')[-1]}_Resume.txt"
    with open(fileName, "a") as f:
        outputHeader(f)
        outputRows(f)
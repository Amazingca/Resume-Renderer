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

def constructData():
    with open("./config.txt") as data:
        rowType = ""
        newRow = False
        for line in data:
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
            elif rowType == "ROW":
                if "ROWS" not in config:
                    config["ROWS"] = []
                isBullet = line.split("=")[0] == "bullets"
                if newRow == True:
                    config["ROWS"].append({
                        line.split("=")[0]: line.split("=")[1] if not isBullet else line.split("=")[1].split(",,")
                    })
                    newRow = False
                else:
                    config["ROWS"][-1][line.split("=")[0]] = line.split("=")[1] if not isBullet else line.split("=")[1].split(",,")

def sectionDivider(f):
    print(config["VARIABLES"]["delimiter"] * config["VARIABLES"]["width"], file=f)

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
            case "pronouns":
                continue        
            case "email":
                continue
            case _:
                print(config["PROFILE"][key], file=f)

    sectionDivider(f)

def outputRows(f):
    for row in config["ROWS"]:
        titleRight = row['titleRight'] if 'titleRight' in row else ''
        descriptionRight = row['descriptionRight'] if 'descriptionRight' in row else ''
        print(f"""{row["title"].upper()}{f"{titleRight:>{config['VARIABLES']['width'] - len(row['title'])}}"}""", file=f)
        print(f"""{row["description"]}{f"{descriptionRight:>{config['VARIABLES']['width'] - len(row['description'])}}"}""", file=f)
        for line in row["body"].split("\\n"):
            print("\n".join(cropWidth(line, "")), file=f) # Print each newline independant from cutoffs when cropping
        for bullet in row["bullets"]:
            print("\n".join(cropWidth(bullet, config['VARIABLES']['bullet'])), file=f)
        sectionDivider(f)

def cropWidth(line, newLineSpacer):
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
    constructData()
    print(f"Creating Resume{': ' if 'title' in config['VARIABLES'] else ''}", end="" if "title" in config["VARIABLES"] else "\n")
    if "title" in config["VARIABLES"]:
        print(config["VARIABLES"]["title"])
    with open(f"./{config['PROFILE']['name'].split(' ')[-1]}_Resume_{date.today()}.txt", "a") as f:
        outputHeader(f)
        outputRows(f)
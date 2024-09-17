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

def outputHeader(f):
    for key in config["PROFILE"]:
        if key == "email":
            if config["VARIABLES"]["isOnline"] == "false":
                print(config["PROFILE"][key], file=f)
            else:
                print(config["PROFILE"][key].replace("@", config["VARIABLES"]["onlineDelimiter"]), file=f)
        else:
            print(config["PROFILE"][key], file=f)
    sectionDivider(f)

if __name__ == "__main__":
    constructData()
    print(f"Creating Resume{': ' if 'title' in config['VARIABLES'] else ''}", end="" if "title" in config["VARIABLES"] else "\n")
    if "title" in config["VARIABLES"]:
        print(config["VARIABLES"]["title"])
    with open(f"./{config['PROFILE']['name'].split(' ')[-1]}_Resume_{date.today()}.txt", "a") as f:
        outputHeader(f)
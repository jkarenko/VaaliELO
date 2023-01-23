# /html/body/div[2]/main/div[1]/div[1]/div/div[2]/div/section[1]/div/div
import json

DEFAULT_RANKING = 1600


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def extract_data(json_file):
    data = load_json(json_file)
    # extract all election promises
    candidates = []
    for entry in data:
        # print(entry["id"])
        candidates.append({"id": entry["id"], "promises": []})
        # add ranking to candidates
        candidates[-1]["ranking"] = DEFAULT_RANKING
        for key in entry["info"]:
            if "election_promise_" in key:
                # print(entry["info"][key]["fi"])
                candidates[-1]["promises"].append(entry["info"][key]["fi"])
    return candidates


def main():
    src = "json/candidates1.json"
    candidates = extract_data(src)
    print(candidates[0:2])
    write_json(f"{src}_promises.json", candidates)


if __name__ == "__main__":
    main()

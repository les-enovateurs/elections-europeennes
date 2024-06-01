import json
import yaml

def extract_urls(json_data):
    urls = []
    for obj in json_data["data"]:
        if "website_url" in obj and obj["website_url"]:
            urls.append(obj["website_url"][0])
    return urls

def convert_to_yaml(urls):
    yaml_data = {
        "urls": [{"url": url} for url in urls]
    }
    return yaml.dump(yaml_data)

def main():
    # Lecture du fichier JSON depuis un fichier
    with open('./data/refacto/programme-website-custom-url.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        urls = extract_urls(data)
        yaml_data = convert_to_yaml(urls)
        print(yaml_data)
        # https://github.com/les-enovateurs/dashlord

if __name__ == "__main__":
    main()

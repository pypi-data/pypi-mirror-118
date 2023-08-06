import sys
import xmltodict
import json
import hashlib
import xml.etree.cElementTree as ET


def guaranteed_list(x):
    if not x:
        return []
    elif isinstance(x, list):
        return x
    else:
        return [x]


def guaranteed_first(x):
    return guaranteed_list(x)[0]


def severity_from_priority(priority):
    return {
        priority > 0: 'info',
        priority > 2: 'minor',
        priority > 4: 'major',
        priority > 6: 'critical',
        priority > 8: 'blocker'
    }[True]


def clear_file_path(path, prefix):
    return path[path.startswith(prefix) and len(prefix):]


def parse_xml(xml_gradle_file, prefix):
    data = []

    xml_tree = ET.parse(xml_gradle_file)
    root = xml_tree.getroot()
    to_string = ET.tostring(root, encoding='UTF-8', method='xml')
    xml_to_dict = xmltodict.parse(to_string)

    for i in guaranteed_list(xml_to_dict['issues']['issue']):

        path = guaranteed_first(i['location'])['@file']
        cleared_path = clear_file_path(path=path, prefix=prefix)

        issue = {
            "description": i['@summary'],
            "severity": severity_from_priority(int(i['@priority'])),
            "fingerprint": hashlib.md5((i['@summary'] + cleared_path).encode('utf-8')).hexdigest(),
            "location": {
                "path": cleared_path,
            }
        }

        if '@line' in i['location']:
            issue["location"]["lines"] = {
                "begin": i['location']['@line']
            }
        data.append(issue)

    return json.dumps(data)


def main():
    with open(sys.argv[1], 'r') as my_file:
        parsed = parse_xml(my_file, sys.argv[2])
        print(parsed)


if __name__ == "__main__":
    main()

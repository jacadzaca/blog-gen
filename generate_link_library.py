#!/usr/bin/python3
import json
import argparse
from typing import Any
from dataclasses import dataclass
from jinja2 import Environment, PackageLoader

@dataclass
class Link():
    name: str
    url: str
    has_children: bool = False

@dataclass
class Folder():
    name: str
    children: Any
    has_children: bool = True

def main():
    parser = argparse.ArgumentParser(description='Transform a bookmark file into a simple webpage')
    parser.add_argument('path', type=str, help='path to the Bookmark file')
    parser.add_argument('--output', type=str, default='bookmarks.html')
    argv = parser.parse_args()
    with open(argv.path) as f, open(argv.output, 'w') as page_f:
        env = Environment(
            loader=PackageLoader('__main__', './templates'),
            trim_blocks=True,
            lstrip_blocks=True)
        raw_bookmarks = json.load(f)['roots'] ['bookmark_bar']['children']
        bookmarks = [to_bookmark(element) for element in raw_bookmarks]
        template = env.get_template('link_library.jinja.html')
        page_f.write(template.render(bookmarks=bookmarks))

def to_bookmark(json):
    if json['type'] == 'folder':
        children = [to_bookmark(element) for element in json['children']]
        return Folder(json['name'], children)
    elif json['type'] == 'url':
        return Link(json['name'], json['url'])
    else:
        raise ValueError(f"Cannot create a bookmark of type {json['type']}")

if __name__ == '__main__':
    main()


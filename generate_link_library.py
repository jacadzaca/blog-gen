#!/usr/bin/python3
import json
import argparse
from typing import Any
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader


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


def to_bookmark(json):
    if json['type'] == 'folder':
        children = [to_bookmark(element) for element in json['children']]
        return Folder(json['name'], children)
    elif json['type'] == 'url':
        return Link(json['name'], json['url'])
    else:
        raise ValueError(f"Cannot create a bookmark of type {json['type']}")


def generate_link_library(bookmarks_path, output_path):
    with open(bookmarks_path) as bookmark_f, open(output_path, 'w') as page_f:
        env = Environment(
            loader=FileSystemLoader('./templates'),
            trim_blocks=True,
            lstrip_blocks=True)

        raw_bookmarks = json.load(bookmark_f)['roots']['bookmark_bar']['children']
        bookmarks = [to_bookmark(element) for element in raw_bookmarks]
        template = env.get_template('link_library.jinja.html')
        page_f.write(template.render(bookmarks=bookmarks))


def main():
    parser = argparse.ArgumentParser(
        description='Transform a bookmark file into a simple webpage')
    parser.add_argument('path', type=str, help='path to the Bookmark file')
    parser.add_argument('--output', type=str, default='bookmarks.html')
    argv = parser.parse_args()
    generate_link_library(argv.path, argv.output)


if __name__ == '__main__':
    main()


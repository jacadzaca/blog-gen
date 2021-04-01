#!/usr/bin/python3
import math
import argparse
from jinja2 import Environment, PackageLoader

def main():
    parser = argparse.ArgumentParser(description='Transform a list of ids of images uploaded to Google Drive into a simple website')
    parser.add_argument('path', type=str, help='path to the list of image ids, which are separeted with a \\n')
    parser.add_argument('name', type=str, help='how to name the image library?')
    parser.add_argument('description', type=str)
    parser.add_argument('-n', type=int, default=10, help='number of images on website')

    argv = parser.parse_args()
    chunks = []
    with open(argv.path) as f:
        chunk = []
        for identifier in f.readlines():
            if len(chunk) == 10:
                chunks.append(chunk)
                chunk = []
            chunk.append(f'https://drive.google.com/uc?id={identifier}')

    env = Environment(
            loader=PackageLoader('__main__', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    template = env.get_template('image_library.jinja.html')
    for (i, image_urls) in enumerate(chunks):
        with open(f'{argv.name}_library{i}.html', 'w') as f:
            f.write(template.render(urls=image_urls,
                next=(i + 1 if not (i == len(chunks) - 1) else None),
                name=argv.name,
                description=argv.description))

if __name__ == '__main__':
    main()


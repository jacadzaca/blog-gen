#!/usr/bin/python3
import re
import os
import time
import argparse
from dataclasses import dataclass, field
from jinja2 import Environment, PackageLoader

TEXT_REGEX='<p id="post">((.|\n)*)</p>'

@dataclass(order=True)
class Post():
    title: str = field(compare=False)
    file_name: str = field(compare=False)
    text: str = field(compare=False)
    date: str

def main():
    parser = argparse.ArgumentParser(description='creates a blog feed page, a rss feed and the lates posts section in the index.html')
    parser.add_argument('posts', nargs='+', help='list of html files that contain blog posts')
    parser.add_argument('--url', help="website's url, e.g https://example.org/")
    parser.add_argument('--rss', default='rss.xml', help='file to output the rss feed')
    parser.add_argument('--home', default='index.html', help='file to output index.html')
    parser.add_argument('--blog', default='blog.html', help='file to output the blog feed page')

    argv = parser.parse_args()
    posts = []
    for file_name in argv.posts:
        if os.path.isfile(file_name):
            ctime = os.path.getctime(file_name)
            post_date = time.strftime('%a, %d %b %Y %X', time.localtime(ctime))
            post_title = file_name.split('/')[-1].split('.')[0].replace('_', ' ')
            with open(file_name) as f:
                post_text = re.search(TEXT_REGEX, f.read()).group(1)
            posts.append(Post(post_title, file_name, post_text, post_date))
    posts.sort(reverse=True)

    env = Environment(
            loader=PackageLoader('__main__', './templates'),
            trim_blocks=True,
            lstrip_blocks=True)
    with open(argv.rss, 'w') as rss_f, open(argv.blog, 'w') as blog_f:
        rss = env.get_template('rss.jinja.xml').render(url=argv.url, posts=posts[:9])
        rss_f.write(rss)
        blog = env.get_template('blog.jinja.html').render(posts=posts)
        blog_f.write(blog)
    with open(argv.home, 'w') as home_f:
        home = env.get_template('index.jinja.html').render(posts=posts[:5])
        home_f.write(home)

if __name__ == '__main__':
    main()


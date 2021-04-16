#!/usr/bin/python3
import re
import os
import time
import locale
import argparse
from dataclasses import dataclass
from jinja2 import Environment, PackageLoader

TEXT_REGEX = '<p id="post">((.|\n)*)</p>'


ENV = Environment(
    loader=PackageLoader(__name__, './templates'),
    trim_blocks=True,
    lstrip_blocks=True)


@dataclass
class Post():
    title: str
    id: str
    post_path: str
    text: str
    date: str


def read_posts(paths):
    """
    creates a list of Posts from a list of html files. Post's content must be in a
    <p> tag with an "post" id
    """
    posts = []
    for c_time, post_path in sorted(zip(map(os.path.getctime, paths), paths), reverse=True):
        if os.path.isfile(post_path):
            post_date = time.strftime(
                '%a, %d %b %Y %X', time.localtime(c_time))
            post_id = post_path.split('/')[-1].split('.')[0]
            post_title = post_id.replace('_', ' ')
            with open(post_path) as f:
                post_text = re.search(TEXT_REGEX, f.read()).group(1)
            posts.append(Post(post_title, post_id,
                              post_path, post_text, post_date))
    return posts


def generate_blog(posts_paths, rss_path, blogs_path, home_path, url):
    posts = read_posts(posts_paths)
    with open(rss_path, 'w') as rss_f, open(blogs_path, 'w') as blog_f, open(home_path, 'w') as home_f:
        rss = ENV.get_template('rss.jinja.xml').render(
            url=url, posts=posts[:9])
        rss_f.write(rss)

        blog = ENV.get_template('blog.jinja.html').render(posts=posts)
        blog_f.write(blog)

        home = ENV.get_template('index.jinja.html').render(posts=posts[:5])
        home_f.write(home)


def main():
    parser = argparse.ArgumentParser(
        description='creates a blog feed page, a rss feed and the lates posts section in the index.html')
    parser.add_argument('posts', nargs='+',
                        help='list of html files that contain blog posts')
    parser.add_argument(
        '--url', help="website's url, e.g https://example.org/")
    parser.add_argument('--rss', default='rss.xml',
                        help='file to output the rss feed')
    parser.add_argument('--home', default='index.html',
                        help='file to output index.html')
    parser.add_argument('--blog', default='blog.html',
                        help='file to output the blog feed page')
    parser.add_argument('--locale', default=None, help="see man locale" )

    argv = parser.parse_args()
    if argv.locale != None:
        locale.setlocale(locale.LC_TIME, argv.locale)
    generate_blog(argv.posts, argv.rss, argv.blog, argv.home, argv.url)


if __name__ == '__main__':
    main()


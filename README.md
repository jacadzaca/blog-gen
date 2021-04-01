# About

Python scripts I use to generate my [website](http://jacadzaca.github.io/)

##  Usage
```bash
usage: generate_blog.py [-h] [--url URL] [--rss RSS] [--home HOME] [--blog BLOG] posts [posts ...]

creates a blog feed page, a rss feed and the lates posts section in the index.html

positional arguments:
  posts        list of html files that contain blog posts

optional arguments:
  -h, --help   show this help message and exit
  --url URL    website's url, e.g https://example.org/
  --rss RSS    file to output the rss feed
  --home HOME  file to output index.html
  --blog BLOG  file to output the blog feed page

usage: generate_image_library.py [-h] [-n N] path name description

Transform a list of ids of images uploaded to Google Drive into a simple website

positional arguments:
  path         path to the list of image ids, which are separeted with a \n
  name         how to name the image library?
  description

optional arguments:
  -h, --help   show this help message and exit
  -n N         number of images on website

usage: generate_link_library.py [-h] [--output OUTPUT] path

Transform a bookmark file into a simple webpage

positional arguments:
  path             path to the Bookmark file

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT
```


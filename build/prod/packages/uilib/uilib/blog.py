
import os
import pandas as pd
import datetime
from flask import url_for
import json

class Blog():

    def __init__(self, article_dir) -> None:
        self.article_dir = article_dir

    def find_all_files_with_extension(self, base_dir, ext=".json"):
        found_files = []  # Renamed from 'files' to avoid shadowing
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(ext):
                    found_files.append(os.path.join(root, file))
        return found_files

    def load_json_file(self, file):
        with open(file, "r") as f:
            data = json.load(f)
        return data

    def get_file_datetime(self, file):
        return datetime.datetime.fromtimestamp(os.path.getmtime(file))

    # input: /app/blog/articles/a5
    # output: a5
    def get_last_path_segment(self, path):
        return os.path.basename(path)

    def get_blog_post(self, slug):
        posts_df = self.get_blog_posts_df()
        row = posts_df.loc[slug]

        post_fn = row["post_fn"]
        img_src = row["img_src"]
        # post_data = self.get_post_data_from_file(post_fn)
        # img_src = row["img_src"]
        # date_str = row["date"].strftime("%B %d, %Y")
        # post_data["date"] = date_str
        # post_data["img_src"] = img_src
        article_dct = self.load_json_file(post_fn)
        article_dct["img_src"] = img_src
        article_dct["date"] = row["date"].strftime("%B %d, %Y")
        return article_dct

    # Read v3 formatted JSON
    def _get_info_v3(self, article_dct):
        article_date_str = article_dct.get("date", '2025-01-01')
        article_date = datetime.datetime.strptime(article_date_str, "%Y-%m-%d")
        intro = article_dct.get("hook", '')
        title = article_dct.get("title", None)
        return title, article_date, intro


    def get_blog_posts_df(self):

        blog_dir = self.article_dir

        if not os.path.exists(blog_dir):
            print("Blog directory does not exist: ", blog_dir)
            return pd.DataFrame()

        with os.scandir(blog_dir) as entries:
            subdirs = [entry.path for entry in entries if entry.is_dir()]

        now_dt = datetime.datetime.now() - datetime.timedelta(days=1)

        posts_df = pd.DataFrame()
        #print("Subdirs: ", subdirs)
        for subdir in subdirs:
            #print("Subdir: ", subdir)

            article_fn = os.path.join(subdir, "article.json")
            if not os.path.exists(article_fn):
                print("Article file does not exist: ", article_fn)
                continue

            article_dct = self.load_json_file(article_fn)
            article_format =  article_dct.get("format", None)

            assert article_format is not None, "Article format is not set, file: %s" % article_fn
            #print("Article data: ", article_dct)

            # files = self.find_all_files_with_extension(subdir, ext=".json")
            # #print("Files: ", files)

            # if len(files) == 0:
            #     continue

            # post_fn = files[0]
            # post_data = self.get_post_data_from_file(post_fn)
            # #print("Post data: ", post_data)


            #slug = post_fn.replace(".json", "")
            slug = subdir.replace(blog_dir, "")
            slug = slug.replace("/", "")
            #print("Slug: ", slug)

            article_slug = self.get_last_path_segment(subdir)

            image_fn = os.path.join(subdir, "image.jpg")
            if not os.path.exists(image_fn):
                blog_image_url = None
            else:
                blog_image_url = url_for("blog.blog_image_serve_page", article_slug=article_slug)

            #print("Blog image url: ", blog_image_url)
            # if "date" in article_dct:
            #     date_str = article_dct["date"]
            #     date_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # else:
            #     date_dt = self.get_file_datetime(article_fn)

            #articles = len(posts_df)
            #days = articles * 7
            #date_dt = ref_dt - datetime.timedelta(days=days)

            # headline = article_dct.get("title", None)
            # if headline is None:
            #     continue


            #print("Article Dct:\n", json.dumps(article_dct, indent=4))

            # if article_format == "v2":
            #     intro_section = article_sections[0]
            #     intro = intro_section.get("text", "")
            # else:
            #intro = intro_paragraph.get("paragraph", "")

            article_sections = article_dct.get("sections", [])

            if article_format == "v3":
                title, article_date, intro = self._get_info_v3(article_dct)
            else:
                title = article_dct.get("title", None)
                article_date_str = article_dct.get("date", '2025-01-01')
                article_date = datetime.datetime.strptime(article_date_str, "%Y-%m-%d")
                first_section = article_sections[0]
                intro = first_section.get("text", '')

            if article_date > now_dt:
                print("Article date is in future: ", article_date)
                continue



            #print("Article\n", json.dumps(article_dct, indent=4))
            posts_df.at[slug, "title"] = title
            posts_df.at[slug, "date"] = article_date
            posts_df.at[slug, "intro"] = intro
            posts_df.at[slug, "img_src"] = blog_image_url
            posts_df.at[slug, "post_fn"] = article_fn

        #print("Posts DF:\n", posts_df)

        if len(posts_df) > 0:
            posts_df = posts_df.sort_values(by="date", ascending=False)
        #print("Posts DF: ", posts_df)
        return posts_df
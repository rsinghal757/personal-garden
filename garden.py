from fasthtml.common import *
from monsterui.all import render_md, Slider
import os
from datetime import datetime
import random

# Initialize the FastHTML app
app, rt = fast_app(live=True)

### FUNCTIONS ###

# Define the base HTML template using TailwindCSS
def base_template(page_title, content):
    return Html(
        Head(
            Title(page_title),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/uikit@3.16.26/dist/css/uikit.min.css"),
            Script(src="https://cdn.jsdelivr.net/npm/uikit@3.16.26/dist/js/uikit.min.js"),
            Script(src="https://cdn.jsdelivr.net/npm/uikit@3.16.26/dist/js/uikit-icons.min.js"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
        ),
        Body(
            Div(
                content,
                cls="bg-[#f9f8f6] text-gray-900 min-h-screen pt-16 pb-12 p-36 font-serif flex flex-col items-stretch"
            )
        ),
    )

# Function to read and parse blog posts
def get_blog_posts():
    posts = []
    for filename in os.listdir("blogs"):
        if filename.endswith(".md"):
            with open(f"blogs/{filename}", "r") as f:
                content = f.read()
                parts = content.split("---", 2)
                metadata, content = (parts[1].strip(), parts[2].strip())
                meta_dict = {k.strip(): v.strip().strip('"') for k, v in (line.split(":", 1) for line in metadata.splitlines() if ":" in line)}
                posts.append({
                    "title": meta_dict.get("title", "Untitled"),
                    "date": meta_dict.get("date", "Unknown Date"),
                    "summary": content.split("\n\n")[0] if content else "",
                    "filename": filename
                })
    return sorted(posts, key=lambda x: datetime.strptime(x["date"], "%B %d, %Y") if x["date"] != "Unknown Date" else datetime.min, reverse=True)

# Function to get projects
def get_projects():
    return [
        {
            "title": "babyARC",
            "description": "A tiny abstraction and reasoning dataset.",
            "link": "https://github.com/rsinghal757/babyARC",
            "images": ["assets/pebble.png", "assets/pebble.png", "assets/pebble.png", "assets/pebble.png", "assets/pebble.png"],
        },
        {
            "title": "SAP-1 CPU Emulator",
            "description": "A Simple As Possible (SAP-1) based CPU emulator.",
            "link": "https://github.com/rsinghal757/sap-1",
            "images": ["assets/pebble.png", "assets/pebble.png", "assets/pebble.png", "assets/pebble.png", "assets/pebble.png"],
    },
    ]

# Function to get social links
def get_social_links():
    return [
        {"platform": "Twitter", "url": "https://x.com/0xRohitSinghal"},
        {"platform": "GitHub", "url": "https://github.com/rsinghal757"},
        {"platform": "Medium", "url": "https://medium.com/@rsinghal757"},
        {"platform": "Writing", "url": "/blogs"},
    ]

### Routes ###

# Blog posts list
@rt("/blogs")
def get():
    posts = get_blog_posts()
    body_content = Div(
        Div(
            Div(
                H1("Blog Posts", cls="text-5xl font-serif mb-12 leading-tight"),
                cls="flex items-baseline space-x-6"
            ),
            *[Div(
                H3(post["title"], cls="text-2xl font-medium font-serif"),
                P(post["date"], cls="text-gray-500 text-lg italic mb-8"),
                P(post["summary"], cls="text-gray-700 text-lg mb-8"),
                A("Read More →", href=f"/blogs/{post['filename']}", cls="text-gray-600 hover:underline text-lg"),
                cls="mb-8 border-b pb-8"
            ) for post in posts],
            cls="mb-12"
        ),
        cls="max-w-7xl w-full leading-relaxed"
    )
    return base_template("Blog Posts", body_content)

# Blog post reader
@rt("/blogs/{filename}")
def get(filename: str):
    filepath = f"blogs/{filename}"
    if not os.path.exists(filepath):
        return base_template("404 - Not Found", Div(H1("404 - Not Found"), cls="text-4xl font-bold text-center"))
    
    with open(filepath, "r") as f:
        content = f.read()
        parts = content.split("---", 2)
        metadata, content = (parts[1].strip(), parts[2].strip()) if len(parts) >= 2 else ("", parts[0].strip())
        meta_dict = {k.strip(): v.strip().strip('"') for k, v in (line.split(":", 1) for line in metadata.splitlines() if ":" in line)}
        title = meta_dict.get("title", "Untitled")
        date = meta_dict.get("date", "Unknown Date")
        html_content = render_md(content)

    body_content = Div(
        H1(title, cls="text-5xl font-medium font-serif mb-12 leading-tight"),
        P(date, cls="text-gray-500 text-lg italic mb-8"),
        Div(html_content, cls="prose prose-lg max-w-7xl leading-relaxed"),
        cls="max-w-7xl w-full leading-relaxed"
    )
    return base_template(title, body_content)

# Homepage route
@rt("/")
def get():
    projects = get_projects()
    social_links = get_social_links()
    body_content = Div(
        Div(
            Div(
                H3("Rohit Singhal", cls="text-5xl font-bold font-serif leading-tight"),
                Div(
                    *[A(link["platform"], href=link["url"], cls="text-gray-600 font-serif hover:underline") for link in social_links],
                    cls="flex flex-row text-gray-500 items-stretch w-full justify-between"
                ),
                cls="flex flex-col items-left space-y-2"
            ),
            Div(
                H3("The world is a museum of passion projects.", cls="text-gray-900 font-serif text-lg italic"),
                Div(
                    A("John Collison", href="https://x.com/collision/status/1529452415346302976", cls="text-gray-500 italic text-right"),
                    P(", Stripe", cls="text-gray-500 italic text-right"),
                    cls="flex flex-row items-end"

                ),
                cls="flex flex-col items-end space-y-0"
            ),
            cls="flex justify-between items-center mb-16"
        ),
        Div(
            H2("What I'm working on", cls="text-3xl font-medium font-serif border-b pb-8 text-left"),
            *[Div(
                Div(
                    Div(
                        H3(project["title"], cls="text-2xl font-medium font-serif"),
                        P(project["description"], cls="text-gray-500 text-lg"),
                        cls="flex flex-col items-left space-y-2"
                    ),
                    A("View Project →", href=project["link"], cls="text-gray-600 hover:underline text-lg"),
                    cls="flex flex-col items-stretch justify-between w-1/3"
                ),
                Slider(
                    *[Img(src=image) for image in project["images"]],
                    cls="w-2/3 h-auto rounded-lg",
                    nav=True,
                ),
                cls="border-b pb-16 pt-16 flex flex-row items-left justify-between space-x-16"
            ) for project in projects],
            cls="p-0 mb-24"
        ),
        cls="max-w-7xl w-full leading-relaxed"
    )
    return base_template("Rohit Singhal", body_content)

# Run the app on port 5001
serve(port=5001)

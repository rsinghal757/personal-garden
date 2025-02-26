from fasthtml.common import *
from monsterui.all import render_md
import os
from datetime import datetime

# Initialize the FastHTML app
app, rt = fast_app()

# Define the base HTML template using TailwindCSS
def base_template(page_title, content):
    return Html(
        Head(
            Title(page_title),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
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
        {"title": "babyARC", "description": "A tiny abstraction and reasoning dataset.", "link": "https://github.com/rsinghal757/babyARC", "images": ["img1.jpg", "img2.jpg", "img3.jpg"]},
        {"title": "SAP-1 CPU Emulator", "description": "A Simple As Possible (SAP-1) based CPU emulator.", "link": "https://github.com/rsinghal757/sap-1", "images": ["img4.jpg", "img5.jpg", "img6.jpg"]},
    ]

# Function to get social links
def get_social_links():
    return [
        {"platform": "Twitter", "url": "https://x.com/0xRohitSinghal"},
        {"platform": "GitHub", "url": "https://github.com/rsinghal757"},
        {"platform": "Medium", "url": "https://medium.com/@rsinghal757"},
        {"platform": "Writing", "url": "/blogs"},
    ]

# Blog posts list
@rt("/blogs")
def get():
    posts = get_blog_posts()
    body_content = Div(
        Div(
            Div(
                H1("Blog Posts", cls="text-5xl font-bold mb-6 leading-tight"),
                cls="flex items-baseline space-x-6"
            ),
            *[Div(
                H3(post["title"], cls="text-2xl font-medium"),
                P(post["date"], cls="text-gray-500 text-lg italic mb-8"),
                P(post["summary"], cls="text-gray-700 text-lg"),
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
        H1(title, cls="text-5xl font-bold mb-6 leading-tight"),
        P(date, cls="text-gray-500 text-lg italic mb-8"),
        Div(html_content, cls="prose prose-lg max-w-3xl leading-relaxed"),
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
                H3("Rohit Singhal", cls="text-5xl font-bold"),
                Div(
                    *[A(link["platform"], href=link["url"], cls="text-gray-600 hover:underline") for link in social_links],
                    cls="flex space-x-8 text-gray-500"
                ),
                cls="flex flex-col items-left space-y-4"
            ),
            Div(
                H3("The world is a museum of passion projects.", cls="text-lg italic"),
                Div(
                    A("- John Collison", href="https://x.com/collision/status/1529452415346302976", cls="text-gray-500 italic text-right"),
                    P(", Stripe", cls="text-gray-500 italic text-right"),
                    cls="flex flex-row items-end"

                ),
                cls="flex flex-col items-end space-y-1"
            ),
            cls="flex justify-between items-center mb-12"
        ),
        Div(
            H2("What I'm working on", cls="text-4xl font-semibold mb-8 text-left"),
            *[Div(
                H3(project["title"], cls="text-2xl font-medium"),
                P(project["description"], cls="text-gray-700 text-lg"),
                Div(
                    *[Img(src=image, cls="h-48 w-auto inline-block mx-1") for image in project["images"]],
                    cls="flex items-center space-x-4 overflow-x-auto"
                ),
                A("View Project →", href=project["link"], cls="text-gray-600 hover:underline text-lg"),
                cls="mb-8 border-b pb-8"
            ) for project in projects],
            cls="mb-12"
        ),
        cls="max-w-7xl w-full leading-relaxed"
    )
    return base_template("Rohit Singhal", body_content)

# Run the app on port 5001
serve(port=5001)

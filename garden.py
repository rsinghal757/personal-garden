from fasthtml.common import *
import markdown
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
                cls="bg-gray-100 text-gray-900 min-h-screen p-6"
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
                metadata, content = (parts[1].strip(), parts[2].strip()) if len(parts) >= 2 else ("", parts[0].strip())
                meta_dict = {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in metadata.splitlines() if ":" in line)}
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
        {"title": "babyARC", "description": "A tiny abstraction and reasoning dataset.", "link": "https://github.com/rsinghal757/babyARC"},
        {"title": "SAP-1 CPU Emulator", "description": "A Simple As Possible (SAP-1) based CPU emulator.", "link": "https://github.com/rsinghal757/sap-1"},
    ]

# Function to get social links
def get_social_links():
    return [
        {"platform": "Twitter", "url": "https://x.com/0xRohitSinghal"},
        {"platform": "GitHub", "url": "https://github.com/rsinghal757"},
        {"platform": "Medium", "url": "https://medium.com/@rsinghal757"},
    ]

# Homepage route
@rt("/")
def get():
    posts = get_blog_posts()
    projects = get_projects()
    social_links = get_social_links()
    body_content = Div(
        Div(
            H3("Rohit Singhal", cls="text-2xl font-bold"),
            Div(
                *[A(link["platform"], href=link["url"], cls="text-blue-500 hover:underline") for link in social_links],
                cls="flex space-x-4 mt-2"
            ),
            cls="bg-white p-6 shadow rounded-lg mb-6"
        ),
        Div(
            H2("Featured Projects", cls="text-xl font-bold mb-4"),
            *[Div(
                H3(project["title"], cls="font-semibold"),
                P(project["description"], cls="text-gray-700"),
                A("View Project →", href=project["link"], cls="text-blue-500 hover:underline"),
                cls="bg-white p-4 shadow rounded-lg mb-4"
            ) for project in projects],
            cls="mb-6"
        ),
        cls="max-w-3xl mx-auto"
    )
    return base_template("Rohit Singhal", body_content)

# Run the app on port 5001
serve(port=5001)

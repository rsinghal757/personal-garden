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
                cls="bg-[#f9f8f6] text-gray-900 min-h-screen p-12 flex justify-center font-serif"
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
            H3("Rohit Singhal", cls="text-5xl font-bold text-center mb-6"),
            Div(
                *[A(link["platform"], href=link["url"], cls="text-gray-600 hover:underline mx-2") for link in social_links],
                cls="flex justify-center space-x-6 text-lg"
            ),
            cls="mb-12"
        ),
        Div(
            H2("Featured Projects", cls="text-4xl font-semibold mb-8 text-center"),
            *[Div(
                H3(project["title"], cls="text-2xl font-medium"),
                P(project["description"], cls="text-gray-700 text-lg"),
                A("View Project →", href=project["link"], cls="text-gray-600 hover:underline text-lg"),
                cls="mb-8 border-b pb-8"
            ) for project in projects],
            cls="mb-12"
        ),
        Div(
            H2("Recent Blog Posts", cls="text-4xl font-semibold mb-8 text-center"),
            *[Div(
                A(post["title"], href=f"/blog/{post['filename'].replace('.md', '')}", cls="text-2xl font-medium text-gray-600 hover:underline"),
                P(post["summary"], cls="text-gray-700 text-lg mt-2"),
                P(post["date"], cls="text-gray-500 text-md mt-2 italic"),
                cls="mb-8 border-b pb-8"
            ) for post in posts],
        ),
        cls="max-w-3xl w-full leading-relaxed"
    )
    return base_template("Rohit Singhal", body_content)

# Run the app on port 5001
serve(port=5001)

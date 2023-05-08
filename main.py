import openai
from git import Repo 
from pathlib import Path
import shutil
import os
from bs4 import BeautifulSoup as Soup
from PIL import Image
import requests

with open('../key') as f:
    key = f.readline()

openai.api_key = key

PATH_TO_BLOG_REPO = Path("/mnt/56e0741b-9f34-45d7-be54-f01bc909b45a/Documents/Materiales+cursos/OpenAI+Python/Practices/blog-project/.git")

PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)

def update_blog(commit_message='Updates blog'):
    repo = Repo(PATH_TO_BLOG_REPO) # Repo location
    print(repo)
    #git add .
    repo.git.add(all=True)
    #git commit -m ""
    repo.index.commit(commit_message)
    #git push
    origin = repo.remote(name='origin')
    origin.push()


def create_new_blog(title,content,cover_image):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image,PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_content):
        #Write a new HTML file
        with open(path_to_new_content,'w') as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title>{title}</title>\n")
            f.write("</head>\n")

            f.write("<body>\n")
            f.write(f"<img src='{cover_image.name}' alt='cover image'><br>\n")
            f.write(f"<h1>{title}</h1>")
            #OpenAI --> Completion GPT
            f.write(content.replace('\n','<br>\n'))
            f.write("<body>\n")
            f.write("<html>\n")
            print ("blog created")
            return path_to_new_content
    else:
        raise FileExistsError("File already exists, please check again your name")

def check_for_duplicate_links(path_to_new_conntent, links):
    urls = [str(link.get('href')) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))

    return content_path in urls

def write_to_index(path_to_new_content):
    with open(PATH_TO_BLOG/'index.html') as index:
        soup = Soup(index.read())

    links = soup.find_all()    
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content,links):
        raise ValueError("Links already exists!")
    
    link_to_new_blog = soup.new_tag("a",href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]
    last_link.insert_after(link_to_new_blog)

    with open(PATH_TO_BLOG/'index.html','w') as f:
        f.write(str(soup.prettify(formatter='html')))

#random_text_string = "New test!!!! alv"

#with open(PATH_TO_BLOG/"index.html",'w') as f:
 #   f.write(random_text_string)

##Create blog with openAI
def create_prompt(title):
    prompt = """
    Biography:

    My name is Edward and I am a Python developer.

    Blog
    Title:{}
    tags:tech, python,cibersecurity,machine learning
    Summary: I talk about use python in cibersecurit field
    Full Text:  
    """.format(title)

    return prompt

title = "The future of Python and Cibersecurity"

response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=create_prompt(title),
    max_tokens = 1000,
    temperature = 0.7
)

blog_content = response['choices'][0]['text']

#Get an image
def dalle2_prompt(title):
    promp = f"A render showing {title}"
    return promp

response_image = openai.Image.create(
    prompt = dalle2_prompt(title),
    n=1,
    size='512x512'
)

image_url = response_image['data'][0]['url']

def save_image(image_url,file_name): 
    image_res = requests.get(image_url,stream=True)
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw,f)
    else:
        print('Error Loading Image')

    return image_res.status_code

save_image(image_url,file_name='title2.png')
#Image.open('title2.png')

path_to_new_content = create_new_blog(title,blog_content,'title2.png')
print(path_to_new_content)
#print(PATH_TO_CONTENT)

#with open(PATH_TO_BLOG/"index.html") as index:
 #   soup = Soup(index.read())

write_to_index(path_to_new_content)
update_blog()
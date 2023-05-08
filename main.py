import openai
from git import Repo 
from pathlib import Path

with open('../key') as f:
    key = f.readline()

openai.api_key = key

PATH_TO_BLOG_REPO = Path("/mnt/56e0741b-9f34-45d7-be54-f01bc909b45a/Documents/Materiales+cursos/OpenAI+Python/Practices/blog-project/.git")

PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)

def update_blog(commit_message='Updates blog'):
    repo = Repo(PATH_TO_BLOG_REPO) # Repo location

    #git add .
    repo.git.add(all=True)
    #git commit -m ""
    repo.index.commit(commit_message)
    #git push
    origin = repo.remote(name='origin')
    origin.push()

random_text_string = "wdwrdeere ererer edddrer ererewrtew3r  retert  jsjsjswwwjsjsjs"

with open(PATH_TO_BLOG/"index.html",'w') as f:
    f.write(random_text_string)

print(update_blog())

#print(PATH_TO_CONTENT)


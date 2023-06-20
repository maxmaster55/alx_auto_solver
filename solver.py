from github import Github
import os
from pick import pick
from dotenv import load_dotenv
from tqdm import tqdm


load_dotenv()

# get auth from .env file
token = os.getenv("GITHUB_TOKEN")
if not token:
    try:
        token = open("token.txt", "r").read()
    except FileNotFoundError:
        token_file = open("token.txt", "w")
        token = input("Enter your github token: ")
        token_file.write(token)
        token_file.close()


g = Github(token)

repos = ["BrightDaniel/alx-low_level_programming",
         "iAmG-r00t/alx-system_engineering-devops"]

repos_names = [i.split("/")[1] for i in repos]
option, index = pick(repos_names, "Please choose a repo to solve: ")

# get solutions repo
sol_repo = g.get_repo(repos[index])

# get folders in root directory
folders = sol_repo.get_contents(".")

names = [i.name for i in folders if i.type == "dir"]
option, index = pick(names, indicator="=>",
                     title="Please choose a project to solve: ")

# get files in selected folder
files = sol_repo.get_contents(names[index])

# get username from user
try:
    username = open("username.txt", "r").read()
except FileNotFoundError:
    username_file = open("username.txt", "w")
    username = input("Enter your username: ")
    username_file.write(username)
    username_file.close()
# create a folder in my remote repo
my_repo = g.get_repo(f"{username}/alx-low_level_programming")

# add a new folder to my repo with tqdm progress bar
print("Creating folder in your repo...")
for i in tqdm(files):
    my_repo.create_file(
        f"{option}/{i.name}",
        f"Added {i.name}",
        i.decoded_content)
print("Done!")

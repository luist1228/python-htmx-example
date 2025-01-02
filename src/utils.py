from os import listdir
from os.path import isfile, join

import markdown
from markdown_checklist.extension import ChecklistExtension
CONTENT_DIR = "./src/content/"

def get_content_files()-> list[str]:
  files = []
  for f in listdir(CONTENT_DIR):
    if isfile(join(CONTENT_DIR, f)) and '.md' in f:
      files.append(f) 
  return files

def generate_content_files():
  print("hola")
  content_files= get_content_files()
  for file in content_files:
			file_name= file.split(".")[0]
			markdown.markdownFromFile(
				input=CONTENT_DIR+file, 
				output=CONTENT_DIR+file_name+".html",
     		extensions=['tables','fenced_code','markdown_checklist.extension'],
       	tab_length=2)

themes = [
  {
		"Name":  "mocha",
		"Value": "mocha",
	},
  {
		"Name":  "mytheme",
		"Value": "mytheme",
	},
  {
		"Name":  "light",
		"Value": "light",
	},
	{
		"Name":  "dark",
		"Value": "dark",
	},
	# {
	# 	"Name":  "cupcake",
	# 	"Value": "cupcake",
	# },
	# {
	# 	"Name":  "bumblebee",
	# 	"Value": "bumblebee",
	# },
	# {
	# 	"Name":  "emerald",
	# 	"Value": "emerald",
	# },
	{
		"Name":  "corporate",
		"Value": "corporate",
	},
	# {
	# 	"Name":  "synthwave",
	# 	"Value": "synthwave",
	# },
	# {
	# 	"Name":  "retro",
	# 	"Value": "retro",
	# },
	# {
	# 	"Name":  "cyberpunk",
	# 	"Value": "cyberpunk",
	# },
	# {
	# 	"Name":  "valentine",
	# 	"Value": "valentine",
	# },
	# {
	# 	"Name":  "halloween",
	# 	"Value": "halloween",
	# },
	# {
	# 	"Name":  "garden",
	# 	"Value": "garden",
	# },
	# {
	# 	"Name":  "forest",
	# 	"Value": "forest",
	# },
	# {
	# 	"Name":  "aqua",
	# 	"Value": "aqua",
	# },
	# {
	# 	"Name":  "lofi",
	# 	"Value": "lofi",
	# },
	# {
	# 	"Name":  "pastel",
	# 	"Value": "pastel",
	# },
	# {
	# 	"Name":  "fantasy",
	# 	"Value": "fantasy",
	# },
	# {
	# 	"Name":  "wireframe",
	# 	"Value": "wireframe",
	# },
	# {
	# 	"Name":  "black",
	# 	"Value": "black",
	# },
	# {
	# 	"Name":  "luxury",
	# 	"Value": "luxury",
	# },
	# {
	# 	"Name":  "dracula",
	# 	"Value": "dracula",
	# },
	# {
	# 	"Name":  "cmyk",
	# 	"Value": "cmyk",
	# },
	# {
	# 	"Name":  "autumn",
	# 	"Value": "autumn",
	# },
	# {
	# 	"Name":  "business",
	# 	"Value": "business",
	# },
	# {
	# 	"Name":  "acid",
	# 	"Value": "acid",
	# },
	# {
	# 	"Name":  "lemonade",
	# 	"Value": "lemonade",
	# },
	# {
	# 	"Name":  "night",
	# 	"Value": "night",
	# },
	# {
	# 	"Name":  "coffee",
	# 	"Value": "coffee",
	# },
	# {
	# 	"Name":  "winter",
	# 	"Value": "winter",
	# },
	# {
	# 	"Name":  "dim",
	# 	"Value": "dim",
	# },
	# {
	# 	"Name":  "nord",
	# 	"Value": "nord",
	# },
	# {
	# 	"Name":  "sunset",
	# 	"Value": "sunset",
	# },
] 


## PYTHON + HTMX Examples
This is a basic exploratory development project focused on testing practical use cases of HTMX within a python enviroment

The scope of this project is limited to minimal functionality, is not meant to be a template/starter project

### Stack

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - [SQLModel](https://sqlmodel.tiangolo.com) for ORM.
  - [Pydantic](https://docs.pydantic.dev) used by Fastapi for data validation.
  - [Sqlite](https://www.sqlite.org/) as the SQL database.
  - [Jinja](https://jinja.palletsprojects.com/en/stable/) as templating engine.
- 🚀 [**HTMX**](https://htmx.org/) for the frontend.
  - [Tailwind CSS](https://tailwindcss.com/) + [DaisyUI](https://daisyui.com/) for styling.
  
### Requirements

- [uv](https://docs.astral.sh/uv/) for Python package and enviroment management

### Workflow

From base dir install all dependencies with

```console
$ uv sync
$ npm i 
```

Then activate virtual enviroment 
```console
$ source .venv/bin/activate
```

The manually start the development server
```console
$ fastapi dev src/main.py
```

If you are modifying any styles in a separte console run the following command in order to generate the static css for tailwind when any .html files are modified
```console
$ npm run watch
```
# recipes
A website for recipes

## Requirements

Python3:
Install requirements using

```
pip install Django Pillow
```

Need [npm](https://www.npmjs.com/) installed. The best way to manage npm versions is with [nvm](https://github.com/nvm-sh/nvm).
Once you've installed npm you can install the frontend packages.
```
cd frontend; npm install;
```

## Run app for development

First you need to create the [tailwind css](https://tailwindcss.com/) files.

## Build static files

Compile typescript to js
```
npx tsc
```

When changing static files run
```
python manage.py collectstatic
```

## Run
```
python manage.py runserver
```

Then open http://127.0.0.1:8000/recipes
# Watch n Learn

This app is created for visual learners where they can watch instructors instruct while they learn. This website displays courses (free and paid). Users can view free courses and buy paid ones to view the course's video content.

## Demo
Use the [Demo Website](https://tjwatchnlearn.herokuapp.com)

https://user-images.githubusercontent.com/67712127/167648499-78ef8089-1c8b-412b-99b6-3188c9fa99e1.mp4

## Technologies used

**Front-end**

```
- HTML
- CSS
- JavaScript
- Bootstrap
```

**Back-end**

```
- Python (Django)
```

## Features

It has the following functionalities:

- User registration
- Email activation on registration
- Responsiveness
- Easy learning experience
- Payment gateway integration (STRIPE)
- Customized admin panel
- ... and more

## Setup Guide

To get this project up and running, you should have python installed on your computer. Install these fonts also:

- Fonts

```buildoutcfg
Red Rose
Verdana
Montserrat
Dosis
```

- Install requirements

```buildoutcfg
pip install -r requirement.txt
```

- Create a .env file and add the following credentials in it:

```buildoutcfg
SECRET_KEY=
DEBUG=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

- Run the following commands in exact order:

```buildoutcfg
python manage.py migrate
python manage.py runserver
```

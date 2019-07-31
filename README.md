# 500px-challenge

to build:

$ docker-compose build

to run:

$ docker-compose up

then:

$ http localhost

to test:

$ docker-compose run app pytest

## To Do

- [x] css file
- [x] Design page
- [x] Request from popular
- [x] Handle pagination
- [x] ask for only 20
- [x] pagination queryparams
- [x] page links
- [x] Add Details page
- [ ] tests
- [ ] Why does pagination not seem to work near the end?

## Specification

In this challenge we are asking for your help building a simple web
application. The web app will be similar to our own site, and consume content
from the 500px API (we will provide you with an API key and documentation).

During the development of this web app, you may face different design or
implementation choices. You’re free to make any such choices as you see fit;
however, please make sure you document these decisions and include them in your
code as either comments or in a summary included with your submission. We want
to see how you think, what decisions you make, and why.

This challenge is designed for candidates to showcase their learning, problem
solving, and programming skills. There is no strict time limit, but please let
us know your estimation on how long this challenge will take.

### Rules and Tools

To build the web app, you are free to use the technology of your choice,
although we’d recommend React as that is what we use here at 500px. We also
make use of Backbone + Marionette, and Ruby on Rails, so those would also be
good choices. It’s okay to use some third-party libraries or plugins (e.g. npm
modules), but we might ask you the reasons behind your choices.

You must check your solution into Github and maintain a communicative commit
history so that we can follow the evolution of your solution. Also, please put
your documentation in Github wiki pages or a README.md

This challenge is not designed to be difficult, but the code you write should
meet your own high standards. We value thoughtful, clean, concise and clear
code.

### Documentation

All of 500px's API are [documentated on github](https://github.com/500px/legacy-api-documentation). Two you may want to look at are:

- [Photo GET endpoint](https://github.com/500px/legacy-api-documentation/blob/master/endpoints/photo/GET_photos.md)

- [Image Sizes and URLs](https://github.com/500px/legacy-api-documentation/blob/master/basics/formats_and_terms.md#image-urls-and-image-sizes)

### Assessment

Your solution will be assessed before an on-site interview. If you are invited
for an interview, we’ll have some follow-up questions about why you designed
and implemented your app the way you did, and ask questions about how your app
might evolve in different situations.

#### Task 1 - Photo Showcase

Create a simple web app to showcase Popular photos from 500px. Specifically, it
should show photos in our “Popular” feature dynamically obtained from the 500px
API. The list should support pagination, allowing users to browse through
multiple pages of content. Feel free to choose exactly how you’d like to
present the photos based on your own intuition.

#### Task 2 - Photo Details

When user clicks on a photo on the grid, a full screen version of the photo
should be displayed along with more detailed information about the photo, such
as its title, description, and any other data you think might be useful to
display.

#### Task 3 - Cosmetics and Testing

This task is fairly open - further polish your web application and show off
some of your strengths. Some ideas include:

- Use your CSS talent to beautify your UI; improve the style, add animations, etc.
- Increase the reliability of your application by adding extensive test coverage

Feel free to choose the direction you want take (or even do both if you have
extra cycles). Use this opportunity to show us what you’re good at in addition
to coding.

Use this API consumer key in your app: REDACTED Please do NOT commit this key
into public repo. Try to think of a way to import this key dynamically in local
dev only.

# 500px-challenge

You'll need docker compose installed, and a .env file with the following:
```
API_KEY=<a 500px consumer key>
```

to build:
$ docker-compose build

to run:
$ docker-compose up
and then visit http://localhost in a browser

to test:
$ docker-compose run app pytest

No js tests yet :(

## Known issues/limitations

I couldn't figure out why, but the pagination gets weird when you get close to
the final pages. For instance, if there are 407 pages (at a given `rpp` value),
and you request page 410, you'll receive page 407. This isn't really a problem,
as the alternative would just be an error. The weird part is when you start
going *backward* from the end. So if you requested page 405, you still get page
407 (or at least the same photos as on page 407). My first instinct was an
off-by-one error, where the last page should actually be page 406 if there are
407 pages, but as pages are 1-indexed on the 500px api, that shouldn't be the
case. Untimately, I decided not to worry about it as the early pages work
correctly and I didn't want to spend too much time on such a rare use case.

I also ran into some trouble using the `photo_size` queryparam in the api. I
would request a specific size code (3, 30, etc), but I'd only ever get
size-code 22 urls in the `images` field of the response. I tried putting the
size codes in arrays on Pawan's suggestion, but it didn't seem to have any
effect.  To rectify this, I simply used css to re-scale the images on the main
feed page to fit 8 of them on screen. In a real project, this would be at best
a temporary stopgap. As the app is requesting the full-sized images every time
it loads a feed page, page load time will be impacted, as well as using up a
lot of extra bandwidth. Using the pre-set image sizes would also be more
helpful on the layout of the page. I could use cropped square images as
thumbnails, meaning that all thumbnails are the same size, so each 'card' could
have identical dimensions. Instead, I used `max-width` and `max-height` styles
to ensure the images fit on a card *roughly* 300px x 300px, which allowed 8 to
fit nicely on my laptop screen.

This implementation may also run a bit on the slower side, as the
request-response exchange won't complete until the entire request/response sent
to the 500px api completes. In practice, the 500px api is responsive enough
that the additional response overhead is barely noticeable, and the page
doesn't have anything useful to show to the user until that request is
completed anyway, so making the API requests with ajax from a javascript
application would only shift that 'delay' to after the single-page app has
loaded.

## Design summary

I chose to use Flask as my web framework as python is my strongest language by
far, and the requirements didn't seem to require any more advanced
functionality than simple request handling. I was able to make the app (almost)
entirely stateless however, with no need for user accounts or any persisted
data, it can be (almost) entirely functional in nature. The only 'state' that
it needs is the API key and url to the api endpoint (which has a sensible
default... the actual api url).

## React addendum

Since my original submission, I worked on a Reactjs front-end a little bit.
Partially to learn more abour reactjs, and partially because I was bored at my
family's cottage.

The first thing I did was create a simple mock api server (see the mock_api
directory and 'api' container) so that I didn't have to overwhelm a hotspot's
bandwith with hundreds of requests to the 500px API.  How it works is you run
the `dl_mock.py` script, which downloads a snapshot of the 500px api at that
moment, requesting 3 pages of 8. It also downloads the image files and details
payloads for the first 24 images in the popular feed. Then, spinning up the
container sets up a server that mocks the 500px api, rewriting relevant urls to
ones that refer to the local api mock. The images themselves are served via the
nginx container through it's `/content` route. To use the mock api instead of
the real thing, add `API_HOST=http://api` to the .env file (same place the
consumer key goes) This took me about 2 hours.

Next, I set to developing the react app in earnest. I'd already spent about 30
minutes getting a simple page of 8 photos working, so I decided to implement
paging. you can see the code I came up with in the `spa_src/index.js` file. I
didn't have a linter set up for javascript, unfortunately, so it's not my best
work by a long shot, but it works. there isn't a way to choose an arbitrary
page, but you can go back and forth easily.

This is as far as I've gotten. Next up would be implementing the detail page
view, followed by arbitrary paging and tests.

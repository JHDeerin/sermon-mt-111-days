# Sermon on the Mount in 111 Days

A website to assist in memorizing the whole Sermon on the Mount.

It's currently still very much a work-in-progress.

## Build the site

```sh
uv run main.py
```

## Design Plan 

-   Have a `build` folder that'll hold all the output pages - there'll be 111 pages (one for each verse), and an `index.html` homepage that'll have a 1-paragraph intro to the project, a "how to use" section (hopefully 1 paragraph), and then a list of all the pages
-   Things that'll be customized for each page:
    -   Page title element
    -   Page subtitle (`Day X`)
    -   What ESV heading section we're on (`Section 1: The Beatitudes (Matthew 5:1-12)`)
        -   Should be pretty simple, each section has a range of days that'll map to it
    -   The verses to memorize
        -   Here, we need to map each day to a single verse verse - then, figure out what section it belongs to, and the section range to present for that day
        -   IDEA: For verses that should map to a line break `\n`, include the line break in that verse - that way we can just concatenate them all together
        -   Each verse should have the verse itself, and the reference - OH, and the meditation for it
    -   So, something like this:
        ```json
        // site data
        {
            "verses": {
                0: {
                    "text": "Seeing the crowds, he went up on the mountain, and when he had sat down, his disciples came to him.",
                    "reference": "Matthew 5:1",
                    "meditation": {
                        "text": "Spurgeon says things",
                        "author": "C.H. Spurgeon",
                        "sourceTitle": "Matthew 5 Commentary",
                        "sourceLink": "https://stuff.com"
                    }
                }
            },
            "sections": {
                0: {
                    "name": "The Beatitudes",
                    "startVerse": 0,
                    "endVerse": 11
                }
            }
        }
        ```
-   How will I actually populate this?
    -   Should 100% be a way of getting ESV Bible verses (yup, their API)
    -   Okay, now I need to get the meditation - or maybe I should wait on that for now, and get it later

-   Other idea:
    -   Get rid of the Nav (just make people go to the home page if they want to select a specific day, and have the `prev`/`next` buttons if they want to navigate)

-   Copyright stuff:
    -   ESV seems to allow using their verses for non-commercial purposes: https://api.esv.org/
    -   "You must include the standard ESV copyright notice on your site (see below) and identify the passages as coming from the ESV. Each page on which you use the text must include a link to www.esv.org"

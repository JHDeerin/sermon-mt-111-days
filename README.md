# Sermon on the Mount in 111 Days

A website to help people memorize the whole Sermon on the Mount: https://jhdeerin.github.io/sermon-mt-111-days

## Local Installation

```sh
uv sync     # install Python dependencies
npm install # install Jest for JS testing
```

The infrastructure here is pretty quick n' dirty, as this is a very small static site. The actual site builder is written in Python (with [uv](https://docs.astral.sh/uv/getting-started) for dependency management); [Jest](https://jestjs.io/docs/getting-started) is used for testing small bits of Javascript (and is the only reason npm is required - these packages are only used for testing, and aren't used for any of the actual site components).

### Build the Site

```sh
uv run main.py
```

This will create the static HTML files for the site and dump them in the `docs` folder. You can then directly open those HTML files in a browser to preview them (no server required).

### Run Frontend Tests

```sh
npm test
```

For manual testing, open any of the HTML files in `docs` as a file in your browser.

### Deploy

Just push to the `main` branch, and GitHub will deploy the `docs` folder to GitHub Pages.

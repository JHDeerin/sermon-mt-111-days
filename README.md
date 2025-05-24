# Sermon on the Mount in 111 Days

A website to help people memorize the whole Sermon on the Mount: https://jhdeerin.github.io/sermon-mt-111-days

## Local Installation

```sh
uv sync     # install Python dependencies
npm install # install Jest for JS testing
```

The infrastructure here is pretty quick n' dirty, as this is a very small site. The actual site builder is written in Python (with [uv](https://docs.astral.sh/uv/getting-started) for dependency management); [Jest](https://jestjs.io/docs/getting-started) is used for testing small bits of Javascript (and is the only reason npm is required - these are only used for testing, and aren't used for any of the actual site components).

### Build the site

```sh
uv run main.py
```

### Run Frontend Tests

```sh
npm test
```

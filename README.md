# Capy SQLI

## Building and running

```bash
docker build --rm -f Dockerfile -t capy-sqli:latest .
docker run --name capy-sqli --rm -p 29125:29125 capy-sqli:latest
```

## Task

Find the SQL injection

## Walkthrough

The SQL injection exists in the POST request on the page `/search`

Need to use --level=2 for this payload

## Distractors

There is another page with a GET request that functions as a distractor

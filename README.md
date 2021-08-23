## Docker image to be used

`ocdr/custom-serving:cpu-load`

# Usage
- Runs standalone without a transformer
- Expects a json input with tag "image" and base64 value
- Sample file named `data.json` is available in this repo which could be passed as data in cURL request
- Remove `--data-raw` from cURL command and add `--data @data.json -k` at the end of the request

# Working
- stress-ng tool will invoke 80% load on 8 cpu cores
- Timeout is set as 15m

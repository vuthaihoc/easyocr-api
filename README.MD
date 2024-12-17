# EasyOcr Simple Api

## Usage

Run file run.sh

    sh run.sh

- Route `health` check service health
- Route `read` read image and return result from easy ocr with json format

- Options from query

```python
# Lấy các tham số từ query
paragraph = request.args.get('paragraph', 'False').lower() == 'true'
output_format = request.args.get('output_format', 'json')
decoder = request.args.get('decoder', 'greedy')
merge_texts = request.args.get('merge_texts', 'False').lower() == 'true'
```

```bash
curl -X POST -F "file=@text1.png" http://127.0.0.1:5000/read -Lo out.text1.json
curl -X POST -F "file=@text2.png" http://127.0.0.1:5000/read -Lo out.text2.json
```
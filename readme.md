# imgur url extractor
The purpose of the script is to extracting direct urls to the image content of galleries and writes them to an output file. The output file outputs each url on a new line

# supported URLs
- imgur.com/gallery/xxxxx
- imgur.com/a/xxxxx/all
- imgur.com/a/xxxxx

# depedencies
- Python 3
- [httplib2](https://pypi.python.org/pypi/httplib2)

# usage
```
python extractor.py URL_HERE OUTPUT_FILE HERE
```

e.g
```
python extractor.py http://imgur.com/gallery/RBP1h file.txt
```

# Descriptor API

Just a very simple API to describe images using AI

# Usage
#### Note: The AI, especially OCR, can often make mistakes
#### Note: by default the api runs @ port 5000
#### Note: Only .jpg, .jpeg, .png image file formats were tested
## Installation
### Requirements
- Python >=3.13
- Poetry

### Running
Clone the repository
```
git clone https://github.com/fobbidennotis/descriptor-api.git
cd ./descriptor-api/
```

Install dependencies

```
poetry lock
poetry install
```

Run with poetry
```
poetry run python3 main.py
```

## Routes
### [POST] /describe/
#### Accepts JSON: {
    "image": image_binary
}
#### Returns JSON if successful: {
    "description": {
        "ru_text": Russian image text,
        "en_text": English image text,
        "caption": Image caption/summary
    }
}

#### Or JSON upon error: {
    "error": error messsage
}

Example python usage 
```
url = 'http://localhost:5000/describe/' 
image_path = './image.jpg'
 
with open(image_path, 'rb') as img: # read the image in as binary
    files = {'file': (image_path, img, 'image/jpeg')}
    response = requests.post(url, files=files)

print(response.text)  
```


# Contributing
Contributions are always welcome. Please fork the repository and submit a PR with your changes. In the request, explain your changes as much as possible.

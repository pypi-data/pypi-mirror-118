# RZ colorizer lite

This is the lite version of the colorizer using the caffe models from richard Zhang.

## Usage

```python
from colorizer_lite import Colorizer
model = Colorizer()
color_image = Colorizer.pipeline("pathtobwimg.jpg")
# color_image is a np array which can be displayed or saved using opencv
```

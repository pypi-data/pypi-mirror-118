# arbitrary-sr
It's about arbitrary scale image super-resolution. 

# Usage

## Installation

```bash
pip install 

```

## How to use
```python

from arsr import sr
scale = 2.4
sr0    = sr('edsr')
up_img = sr.upsample(numpy_img,scale) # numpy_img {'type':numpy, 'dimension':(H,W,C) } 
```

# method

- ensemble
- MetaSR
- Implicit representation
- UltraSR (Implicit representation + Spatial encoding)
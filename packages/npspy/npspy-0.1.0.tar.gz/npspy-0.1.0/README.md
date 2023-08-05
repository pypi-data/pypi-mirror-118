# npspy
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

npspy is a simple package to calculate [NPS](https://en.wikipedia.org/wiki/Net_promoter_score) (Net Promoter Score).


## Install
```
pip install npspy
```

## Example

```python
import npspy

npspy.categorize(0)  # "detractor"
npspy.categorize(7)  # "passive"
npspy.categorize(9)  # "promoter"

npspy.calculate([0, 7, 9])  # 0
npspy.calculate([7, 9])  # 50
npspy.calculate([0, 7])  # -50
```

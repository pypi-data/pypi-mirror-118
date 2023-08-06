# SharePriceProvider
![Testing](https://github.com/Plebo13/sharepp/actions/workflows/test.yaml/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fb03b5a446ae4a058e483c916e18d06c)](https://www.codacy.com/gh/Plebo13/sharepp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Plebo13/sharepp&amp;utm_campaign=Badge_Grade)
## Installation
The best way to install SharePriceProvider is by using pip:
`pip install sharepp`

All necessary dependencies will be installed by pip.

## Usage
To use SharePriceProvider simply import it into your python project and call the only function available.
```python
import sharepp

print(sharepp.parse_price('NL0000235190'))
```
If you execute the above example you should get the current price for the Airbus share in EUR. Replace the ISIN with your one. Currently supported are company shares and ETFs.



## Kyly is a simple and basic API wrapper for Bitly.

**Installing using pypi:**
```
pip install kyly
```

**Example:**

First generate an access token [here](https://bitly.is/accesstoken).
```
import kyly

#kyly = kyly.KyLy(token='your token here')

kyly = kyly.KyLy(token='')


#x = kyly.shorten("your link here")
#shorten a link
x = kyly.shorten("https://github.com/centipede000")

#print shortened URL
print(x)
```
Output:
```
>>> https://bit.ly/3gMqqnk
```

**The Bitly API has ratelimits, keep those in mind while using.**
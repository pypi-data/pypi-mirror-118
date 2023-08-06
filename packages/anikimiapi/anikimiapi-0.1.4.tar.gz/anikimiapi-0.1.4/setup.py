from setuptools import setup

des = """
<h1 style="text-align: center;">AniKimi API</h1>
<div align="center">A Simple, LightWeight, Statically-Typed Python3 API wrapper for GogoAnime</div>
<div align="center">The v2 of gogoanimeapi (depreciated)</div>
<div align="center">Made with JavaScript and Python3</div>


###

<div align="center">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen">
<img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">
<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
<img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white">
</div>

### 
```
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="dbakbihihrkqnk3",
    auth_token="EKWBIH4NJTO309U4HKTHI39U9TJ5OJ0UU5J9"
)

# Getting Anime Links
anime_link = anime.get_episode_link(animeid="clannad-dub", episode_num=3)

print(anime_link.link_hdp)
print(anime_link.link_720p)
print(anime_link.link_streamsb) # And many more...
```

### Features of AniKimi
* Custom url changing option.
* Statically-Typed, No more annoying JSON responses.
* Autocomplete supported by most IDE's.
* Complete solution.
* Faster response.
* Less CPU consumption.

###
#### For full usage instructions, Head over to the [GitHub Page](https://github.com/BaraniARR/anikimiapi).
"""


setup(
    name='anikimiapi',
    packages=['anikimiapi'],
    version='0.1.4',
    license='LGPLv3+',
    description='A Simple, LightWeight, Statically-Typed Python3 API wrapper for GogoAnime',
    long_description=des,
    long_description_content_type="text/markdown",
    author='BaraniARR',
    author_email='baranikumar2003@outlook.com',
    url='https://github.com/BaraniARR/anikimiapi',
    download_url='https://github.com/BaraniARR/anikimiapi/releases/tag/v0.0.1-beta',
    keywords=['anime', 'gogoanime', 'download', 'sub', 'dub'],
    install_requires=[
        'bs4',
        'requests',
        'requests_html',
        'lxml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

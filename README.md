[![Build Status](https://travis-ci.org/Lacsap-/4scanner.svg?branch=master)](https://travis-ci.org/Lacsap-/4scanner)
# 4scanner

4scanner can search multiple imageboard threads for matching keywords then download all images
to disk.

## Supported imageboards
- 4chan
- lainchan (except lambda for now)
- uboachan

You can create an issue if you want to see other imageboards supported

## Installing

``` pip3 install 4scanner ```

(4scanner is ONLY compatible with python3+)

## How to

the first thing you need to do is create a simple json file with the folders names
you want, the board(s) you want to search and the keywords.
(see the json file section for more details)

After your json file is done you can start 4scanner with:

``` 4scanner file.json ```

it will search all threads for the keywords defined in your json file and
download all images/webms from threads where a keyword is found. (In the current directory unless you specify one with -o )

## Creating your JSON file

Creating the JSON file is easy, you can use the example.json file as a base.

Your "Searches" are what 4scanner use to know which board to check for what keywords and the name of the folder where it needs to download the images, you can have as many "Searches" as you want.

Here is an example of what the JSON file should look like:
```
{"searches":[
    {
      "imageboard":"IMAGEBOARD",
      "folder_name":"YOUR_FOLDER_NAME",
      "board": "BOARD_LETTER",
      "keywords": ["KEYWORD1", "KEYWORD2"]
    },

    {
      "imageboard":"4chan",
      "folder_name":"vidya",
      "board": "v",
      "keywords": ["tf2", "splatoon", "world of tank"]
    }
]}
```

## Notes

- the keywords search is case insentitive

## 4downloader

4downloader is also installed with 4scanner and can be use to download
a single thread like this:
``` 4downloader http://boards.4chan.org/b/thread/373687492 ```

It will download all images until the thread die.
You can also download threads from imageboards other than 4chan with ```-i```

## Tips

Since 4chan and many other imageboards are a cesspool of repost, you will probably download duplicates pictures
very fast. To prevent this you can download fdupes and run it as a cron job to remove duplicates like so:

```fdupes -rdN downloads/```

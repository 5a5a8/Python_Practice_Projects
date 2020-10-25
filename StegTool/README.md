# StegTool
A project I wrote to hide messages and files within PNG images.
It uses Least Significant Bit (LSB) steganography for this.

It was written on a dusty Sunday afternoon and is heavily inspired by [this article.](https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2)

If you're going to be using this for actual steganography, I suggest you encrypt your data before hiding it.

## Encode
Simply enter the name of the image you want to hide the data in.
Also enter the name of the output file - this will be the modified image.
You will then be prompted to write either a message or the name of a file you want to hide - if the file is not found it will treat your input as a message.

## Decode
Enter the name of the image containing hidden data.
Also enter the name of the outfile.
For example if you know the file contains a message you might call this message.txt.
If you know the image contains a zip file you might call this file.zip.

If no message or file is found in the image, it will dump all of the LSB information to your outfile as hex.

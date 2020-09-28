# GoSweetSpot API Demo
This program was written as a kind of proof of concept.
I wanted to show it was possible to create and print shipping labels in GoSweetSpot without logging in.
Their API documentation was not 100% clear to me so I created this program to see if it would work.

It calls the API to create the shipment within your GoSweetSpot account, and returns the shipping label as a PDF.

The payload at the top of the file must be modified to match the shipment, and your own API key should be added in the 'key' variable.

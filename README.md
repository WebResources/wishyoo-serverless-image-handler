# wishyoo-serverless-image-handler

Wishyoo Serverless Image Handler

This python code does two separate things.

1) It creates a webp thumbnail of every jpg or jpeg in the EFS volume. 
2) It creates a webp image from any jpg or jpeg in S3.

The python files starting with "efs" handles reading of the EFS volume and converting the jpgs or jpegs to webp thumbnails.

![Overview](/WebResources/wishyoo-serverless-image-handler/WishyooServerlessImageHandler.drawio-2.png)


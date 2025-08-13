# Chromakey value finder
While deeplearning is amazing at what it does and is often the faster and better solution so cases allow for the use of traditional segmentation methods.

One of these approaches is color based segmentation, also knows as chromakey. however, the process of finding the right color range for the mask can be tricky. On top of this it varies with lighting and shadow effects. This script can be used to help find the right values.

Upon startup it loads the images and applies dictionary of preconfigured masks:

```python
masks = {
    "background": {
        "min": [120, 208, 253],
        "max": [124, 208, 255]
    }
}
```

## How to use
This list can be extended by clicking on pixels with the `left mouse` button.
Clicking the `right mouse` button on the marked point removes it again
Additionally the `m` button can be used to show the new mask and the `esc` is used to exit the program.

The color and masking values are printen after each click to make it easy to recreate the mask.


| Original Image                | Partly Masked Image           |
|-------------------------------|-------------------------------|
| ![Original](images/ChatGPT%20Image.png) | ![Masked](images/partly%20masked%20image.png)           |

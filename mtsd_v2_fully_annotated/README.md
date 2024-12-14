# Mapillary Traffic Sign Dataset

This is the Mapillary Traffic Sign Dataset (MTSD). It contains bounding-box annotations
for traffic sign detection and class labels for traffic sign classification.

A detailed description of the dataset can be found in this technical report:
    https://arxiv.org/abs/1909.04422

# Demo Script

This package includes a demo script to demonstrate how to load and show the annotations
of MTSD. It's a python script and can be executed in a shell as follows:

```
python ./visualize_example.py
```

The python requirements for this script can be found in `requirements.txt`.

# Data Format

The dataset is stored in the following 3 directories.

## Splits

This directory contains text files defining the splits of the dataset. Each split is defined
in a text file (eg. `splits/train.txt`) where each line corresponds to an image. The
filenames of the corresponding image and annotation files are those keys.

## Images

This directory contains the image files with each filename corresponding to an image key.
Example: `images/Bh36Ed4HBJatMpSNnFTgTw.jpg`

The image directory might be shipped in a separate ZIP package.

## Annotations

This directory contains the annotation files with each filename correspondign to an image key.
Example: `annotations/Bh36Ed4HBJatMpSNnFTgTw.json`

The annotations are stored as JSON with the following keys:

 - `width`: the width of the corresponding image
 - `height`: the height of the corresponding image
 - `ispano`: a boolean indicating if the image is a 360° panorama image
 - `objects`: a list of traffic signs in the image

 Each object is itself a dictionary with the following keys:

  - `bbox`: defining the bounding box of the traffic sign within the image.
  - `key`: a unique identifier of the traffic sign.
  - `label`: the class of the traffic sign
  - `properties`: a dictionary defining special properties of the sign.

Please see the demo script for an example of how to load the annotations.

### Panorama handling

Panoramas are stored as standard images with equirectangular projection and can be loaded as any
image.

For the special case of traffic signs that extend across the image boundary of a panorama (`xmin > xmax`),
we include a dictionary `cross_boundary` in the `bbox` defnition containing the `left` and the `right` crop
of the bounding box. In order to extract the full image crop of the traffic sign, one can crop `left` and
`right` separately and stitch them together.

Example: `annotations/OENb8BfFyAocFzHHM4Mehg.json`

### Partially annotated set

The partially annotated set additional includes correspondance information for each object in
the `correspondance` dictionary:

  - `image_key`: the key of the image in the fully annotated set containing the corresponding traffic sign.
  - `object_key`: the key of the corresponding traffic sign object in the fully annotated set. 


# Deep Medical Toolkit (dmt)

This repo consists of a personal code toolkit for the purpose of facilitating medical imaging research. The main components of this library consists of a neural network model zoo, image transformations (for preprocessing &amp; augmentation), common metrics/losses, fast multiprocessed data loading, and data structures for image samples.


## Implementation Details

### Similarities to [Torchio](https://github.com/fepegar/torchio)
 - Same design hierarchy where samples (dict subclass) can hold arbitrary
    attributes, and library-specific data like Images (e.g. ScalarImage3D), 
    Labels (e.g Masks)
 - Transforms take samples (i.e. subjects) as they contain all the abstractions
    and data format conversions built-in. Also their custom attributes feature
    allows for easy storage of transformation history. 

### Improvements Over [Torchio](https://github.com/fepegar/torchio)
 - Overall objects and shift in design..
    - Introduced data abstractions like samples (i.e. subject in torchio) and
    examples (elements in a batch). This distinction is important. 
    - More extensible to allow custom behavior for data structures.  
 - Added general data structures for 2D & 3D images, and labels. 
    - 3D: ScalarMask3D, ScalarImage3D
    - 2D: ScalarMask2D, ScalarImage2D, VectorImage2D
    - Classification: CategoricalLabel
 - Extended transformations to both 2D & 3D. Also added some 3D ones as well.
    - Added 3D transforms:
    - All 2D transforms:
 - Improved existing data structures.
    - For labels, added categorical (both multi-class & multi-label). 
    - For Images, gives you the option to permanently load data. 
    - Extensibility is improved for almost all data structures. For example, in 
    an Image, you can overload how a file is read, what preprocessing you want,
    how to get an array/tensor from the preprocessed sitk image.
 - Extended multiprocessing data loading for better flexibility, extensibility, and performance.
    - Torchio has a Queue class that loades patches, DMT's equivalent of this is the PatchLoader class.
     - This class continously loads patches rather than waiting for the queue to empty.
    - DMT also has a DaemonLoader class that wraps the PyTorch DataLoader to continuously load samples.   
 - Added a model zoo that has both 2D & 3D neural networks.
 - Added losses & metrics common to 2D & 3D computer vision tasks.

Additional Verbose Improvements 
 - Universally, numpy.ndarrays are passed around (instad of tensors like torchio)
 - Sample images (one sample = one patient) are lazy-loaded as an sitk object
if a path is given.


### TODO:
General
- [x] Add weak references for Samples, Images, and Labels for easy access. 
- [ ] Remove printing private attributes in __repr__ for images & others.
- [ ] For samples, and other relevant dict objects, check if reserved_attributes are not being overwritten. 

Data
- [ ] Add mask + image overlap plotting for samples
- [ ] Add 

Transforms
- [ ] Add image shape tracking to attributes for transforms (sample transform history).
- [ ] Add both 2D & 3D resized crop where you can set the scale.

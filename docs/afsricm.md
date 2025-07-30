### Afsricm
#### Cleaning
- Converting files: Convert the raw files to an HDF5 image stack file.

<p align="center">
  <img src="images/afsricm/0_raw-stack.png" height="200"><br>
  <em>Figure 1:</em> Raw image of a cell pressed with AFS and seen with RICM
</p>

- Averaging background:
    First separate the stack in 2 (one with active microrheology images and the other with background frames) by using **frame_keeper** [Figure 2.a].
    Then perform an average along the time axis with the **mean** function [Figure 2.b]
<p align="center">
  <img src="images/afsricm/Background-Average.svg" height="200"><br>
  <em>Figure 2:</em> Averaging of the background stack: a) a frame of the background b) the averaged background
</p>

- Shutter segmentation: Use **otsu_threshhold** on the average background to get the shutter mask [Figure 3.a] then apply **convex_hull** to get the regularised shutter mask [Figure 3.b]
<p align="center">
  <img src="images/afsricm/Extracting shutter mask.svg" height="200"><br>
  <em>Figure 3:</em> Extraction of the shutter mask: a) Mask obtained with otsu threshold b) Morphological transformation with Convex Hull
</p>
- Cropping: **Crop** the AMR stack, the averaged background image and the shutter mask with the bbox of the shutter [Figure 4]
<p align="center">
  <img src="images/afsricm/Cropping inside the shutter.svg" height="200"><br>
  <em>Figure 4:</em> Cropping inside the shutter: a) Cropped AMR stack b) Cropped averaged background image c) Cropped shutter mask
</p>
- Background subtraction: **Subtract** the cropped AMR stack with the cropped averaged background [Figure 5.a] and then use **max_contrast** [Figure 5.b]
<p align="center">
  <img src="images/afsricm/Subtract background.svg" height="200"><br>
  <em>Figure 5:</em> Subtracting the background: a) Background removed stack b) Stack with contrast maximized
</p>

#### Tracking


#### Exctraction

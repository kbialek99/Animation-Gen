# Animation Generating Walkthrough

This is a set of nodes and workflows that allows the user to generate animation in the desired number of frames using InvokeAI.

## What is the general idea?

When making this i had in mind walk animation for 2D game characters, so that would be generating walk animations from views: front, back, side for 4 directional movement. But to be honest it can be used to generate whatever animation you want. I will show the process of making the walk animation mentioned.

Here is how it works (for now):
- The workflow reads rendered images that were made based on 3D objects. Then using openpose processor and mixing it with the renders, frame by frame, it outputs the gif of those images resulting in animation of your liking.

## How to set this up

So to get those things going, apart from what you can download from this repo, you will need a blender scene that will generate the images representing each frame. I recommend this [video](https://www.youtube.com/watch?v=l1Io7fLYV4o).

To sum this up here are the steps you need to follow:
1. Download Blender.
2. Find an .obj witch a RIGGED character that you like (or make one if you can).
3. Upload it to Mixamo and download an animation of your liking.
4. Now when you have a 3D model and an animation, follow the video (more or less) I’ve mentioned above. NOTE: If you can’t rotate the model correctly for each angle, you can set up multiple cameras for each view you want and switch between them instead.
5. TIP: Use black background for the rendered images instead of transparency. The Openpose processor works better this way.
6. See the output images. Check if the model is well-lit. If the shadows are too dark or some limbs are not well visible it might result in clunky outputs from the Openpose node.
7. Play around a little bit with the lighting and see what works best for you.
8. After you check the openpose performance with the selected lightning you can change the background back to transparency.
9. Now you have the input that is necessary for the workflow. I will explain now, how this thing works and how to tame it.

### Here are the major steps in the process:
- After reading the image it is sent to openpose processor to generate pose. Please have in mind though that the results are rarely perfect. It depends a lot on the input image and the visibility of the model as well as on the number of frames. If you generate your animation in 10 FPS then the differences between each frame are rather significant. For 60 FPS differences between each consecutive frame are minor. The more frames the clunkier animation you will get from openpose. That’s why we don’t rely that much on it.
- Before denoising the latent we also pass the raw rendered image into the node.

### Denoising Start
As for the Denoising Start you have two options: If you want more consistent animation set the higher value. If you want the AI to be more creative, set it to lower values. 0.4 is a good start. It allows you to generate some clothes from the prompt on the model while keeping the limb placement according to the input image. 0.5 is better when you overpaint some details on the rendered model, so the clothes are more constant between each frame.

This is the main setting that really matters here. The next part of the workflow is face correction. It has a separate prompt so input there info only about the face.

### Lets see some input - output results along with some settings

| **Input** | **Output**|
|:---:|:---:|
|<img src="./example/input.png" alt="Input Image" width="400"> | <img src="./example/output.png" alt="Output Image" width="400">|

### Result Animation

<img src="./example/outputanim.gif" alt="Output Animation" width="400"> 

As you can see the limb placement is accurate which allows to create pretty decent animations. The main drawback is that some of the features defined in prompt will be ignored. But this is no problem if the input image contains the features described in the prompt. This however will require some manual work for each frame.

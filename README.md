# Robocup Project

### Documents:
1. [Proposal](initial_concept.pdf)
2. [Documentation](documentation.pdf)
3. [Slides](slides.pdf)
4. [Demonstration](demo_video.mp4)

### Flow charts:
![grafik](https://github.com/cornelius-braun/robocup/blob/main/flowchart.png)
Visualization  of the interfaces between the certain components.

To edit the chart: import the flowchart.drawio file on https://app.diagrams.net/, change it, export it as png and don't forget to save changes and reupload the updated .drawio file to github.

The final implementation with threading, to allow executing keyframes while waiting for an end, looks like this: 

![grafik](https://user-images.githubusercontent.com/64356366/125600387-2b986d20-2f8e-43a0-822c-aee43dbde325.png)


### Chosen genres:
- pop/disco
- classic
- metal/rock

## 1.) Sensing
### Record and save the music (with microphone played by external device or use internal stereomix microphone) (Seraphin)
TODO:
- [X] Record music over microphone and stereomix 
- [X] Clean and normalize audio, so that the genre classification works (depends on mic quality. Added file loading option)

## 2.) Thinking
### Process music and choose corresponding genre and dance/keyframes (Cornelius)
TODO:
- [x] Be able to recognize music from file. To do so, either filter training data or change the NN.

## 3.) Acting
### Generate dance moves/keyframes (Emi) 
Take a look at: https://www.youtube.com/watch?v=ikNX8A-3P98
- [X] Implement full dances, choose one based on music?
- [X] Installing software Choregraphe
- [X] Generate keyframes for each genre

## General TODO:
- [x] Determine which genres we want to detect
- [X] Determine the length of the music and the corresponding dace. (= solved by looping dance and stopping dance when music staps)
- [X] Write the full loop 
- [X] Optional: Stop dancing if we stop music

   

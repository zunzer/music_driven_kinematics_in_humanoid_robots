# Robocup Project

### Documents:
1. [Proposal](https://docs.google.com/document/d/139C3r5uC-RRzDMXRm0g1Ai2ML-xSVXDXS0IiixRRfbA/edit?usp=sharing)
2. [Documentation](https://docs.google.com/document/d/1CufPoTXPWW5sYlDkF2OL6iUg1hV41pW2VyHPGJyzTI8/edit?usp=sharing)
3. [Slides](https://docs.google.com/presentation/d/1gnjdcyrNOKNN7O094gugxx_e3Koedi6KGnUoQJ98D0k/edit?usp=sharing)

### Flow chart:
![grafik](https://user-images.githubusercontent.com/64356366/122386702-6c952d00-cf6e-11eb-851c-c7b550f97f2c.png)
Visualization  of the interfaces between the certain components.

To edit the chart: import the flowchart.drawio file on https://app.diagrams.net/, change it, export it as png and don't forget to save changes and reupload the updated .drawio file to github.

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

   

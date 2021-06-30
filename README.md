# Robocup Project

### Documents:
1. [Proposal](https://docs.google.com/document/d/139C3r5uC-RRzDMXRm0g1Ai2ML-xSVXDXS0IiixRRfbA/edit?usp=sharing)
2. [Documentation](https://docs.google.com/document/d/1CufPoTXPWW5sYlDkF2OL6iUg1hV41pW2VyHPGJyzTI8/edit?usp=sharing)
3. [Slides](https://docs.google.com/presentation/d/1gnjdcyrNOKNN7O094gugxx_e3Koedi6KGnUoQJ98D0k/edit?usp=sharing)

### Flow chart:
![grafik](https://user-images.githubusercontent.com/64356366/122386702-6c952d00-cf6e-11eb-851c-c7b550f97f2c.png)
Visualization  of the interfaces between the certain components.

To edit the chart: import the flowchart.drawio file on https://app.diagrams.net/, change it, export it as png and don't forget to save changes and reupload the updated .drawio file to github.   

## 1.) Sensing
### Record and save the music (with microphone played by external device or use internal stereomix microphone) (Seraphin)
TODO:
- [X] Record music over microphone and stereomix 
- [ ] Clean and normalize audio, so that the genre classification works

## 2.) Thinking
### Process music and choose corresponding genre and dance/keyframes (Cornelius)
TODO:
- [ ] Be able to recognize music from file. To do so, either filter training data or change the NN.
- [ ] Optional: Calculate bpm

## 3.) Acting
### Generate dance moves/keyframes (Emi) 
Take a look at: https://www.youtube.com/watch?v=ikNX8A-3P98
- Only generate single movements we can combine? 
- Implement full dances, choose one based on music?

TODO:
- [X] Installing software
- [ ] Generate keyframes for each genre

## General TODO:
- [ ] Determine which genres we want to detect
- [ ] Determine the length of the music and the corresponding dace. 
- [ ] Optional: Change speed of keyframes based on music 
- [ ] Optional: Stop dancing if we stop music
   

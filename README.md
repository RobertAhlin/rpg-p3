# <a id="the-game"></a>Rock, Paper, Scissors - The Game

## Second project at Code Institute

Rock, Paper, Scissors - The Game is constructed to show the use of my knowledge with JavaScript. Together with my skills in HTML and CSS. This is a good old classic game called Rock, Paper, Scissors. The basics is to use one of the elements in order to beat another. Where Rock always beat Scissors, Scissors always beat Paper, and Paper always beat Rock. In this game. A user can choose one of the options to play against the computer (the Robot). The Robot's choice is random using "Math.random()" in JavaScript.

# <a id="table-of-content"></a>Table of Content

- <a href="#the-game">Rock, Paper, Scissors - The Game</a>
- <a href="#table-of-content">Table of Content</a>
- <a href="#demo">Demo</a>
- <a href="#user-experience">User Experience</a>
- <a href="#user-stories">User Stories</a>
  - <a href="#strategy">Strategy</a>
  - <a href="#scope">Scope</a>
  - <a href="#structure">Structure</a>
  - <a href="#skeleton">Skeleton</a>
  - <a href="#surface">Surface</a>
- <a href="#technologies">Technologies</a>
- <a href="#features">Features</a>
- <a href="#finalising">Finalising</a>
- <a href="#more-features">More Features</a>
- <a href="#testing">Testing</a>
  - <a href="#bugs">Bugs</a>
- <a href="#deployment">Deployment</a>
- <a href="#credits">Credits</a>
  - <a href="#acknowledgements">Acknowledgements</a>

# <a id="demo"></a>Demo

<img src="readmefiles/amiresponsive.jpg" alt="Website shown in different devices."><br>

The live link to Heroku can be found here - <a href="https://rpg-p3-40e9a3ed28c2.herokuapp.com/" target="_blank">https://rpg-p3-40e9a3ed28c2.herokuapp.com/</a>

The idea for this project it to make a playable textbased role playing game with a realy humorous twist. 

Use "godmode" as code to try it out. (Without the "".)

# <a id="user-experience"></a>User Experience

The user of this website should be able to try out the concept of playing Rock, Paper, Scissors and practice it against a robot. The game here is just based on luck.

## <a id="user-stories"></a>User stories

A visitor to the site should:

- Get a wow-feeling on the landing page and get interested to try the game.
- Understand the purpose of this website quickly and easily.
- Easily navigate the website.
- Play a game for fun.
- Get an understanding the Rock, Paper, Scissors game.
- Be able to enter cheat code to be able to always win.

### <a id="strategy"></a>Strategy

The goal is to make a well-functioning interesting website. The focus was on making the design a fun, user-friendly and creative site.

### <a id="scope"></a>Scope

For the purpose to show my knowledge in JavaScript, as well as doing something fun. And also add something different like thinking outside the box with the possibility to enter cheat code.

### <a id="structure"></a>Structure

I aimed for a simple website that should contain as little clicks as possible. Also as little scrolling as possible. Even though it's quite easy to scroll up and down on a cell phone I still wanted it to be possible to get a quick overview of the game. I wanted to minimize the usage of Media Queries and have a responsive site by using precent in widths etc.

**Website:**

1. **_Home / Index page:_** Landing page with a hero image. Link to play page and some instructions included.
2. **_Game:_** The game area with clickable images to play.

### <a id="skeleton"></a>Skeleton

The website is designed to be clear and simple. And the site has a simple tree structure with hierarchical flows from top to bottom.

**Wireframe**

For this project I tried the Balsamic to scetch a layout.<br>
<img src="readmefiles/balsamic-idea.jpg" width="40%" alt="First idea done in Balsamic.">

The basic idea is to have it simple with some small 3d effects.<br>
I liked the theme I had in my first project with the rounded corners with different areas.

### <a id="surface"></a>Surface

I was first thinking of to have a background color as the shade of a human skin. But as the skin can really vary in color I decided for "burlywood" after been trying out a couple of colors.
I wanted the page to feel warm and light. So the combination of the burlywood color and the white "clouds" I think I achieved that.

## <a id="technologies"></a>Technologies

1. HTML - To create a basic site
2. CSS - To create a nice, standout front-end with a feel of 3d and shading.
3. JavaScript to handle all the mechanics.

## <a id="features"></a>Features

Existing Features
- Navigation Bar

There is a small navigation bar on the index page. I didn't want another page for the instructions so I made a hidden div that toggles hidden and shown when clicking the Instructions link.
The navigation bar on the game page contains a link back to index page.

A really cool hero image:<br>
<img src="assets/images/hero-image.png" width="50%" alt="Hero image on landing page"><br>
Something eye catching on the page to make the visitor interested.
I  used some skills in Photoshop to make the image.

The first basic structure for the game looks like this:<br>
![First structure.](readmefiles/first-layout.jpg)<br>
This will be the main theme for all and will be added with contents.

My design theme fits well to use a footer. In the footer I placed the ability to enter code.<br>
![Image of the footer](readmefiles/footer.jpg)<br>
It feels like a good place to have the cheat code area. It doesn't interfere with the game design but still it available.

The game area. I wanted it to be simple. At first, I made it possible to first choose what move to play and then click a Play button to start. But after discussion with my mentor, I changed it, so the game starts as soon as the player click a hand. And then a one second wait timer to simulate that the robot is thinking. The score will increase by one up to ten to determine the winner. Then the game has to be restarted by clicking the reset score button.<br>
![Example of some images from the image page](readmefiles/game-area.jpg)

## <a id="finalising"></a>Finalising

<img src="readmefiles/index-image.jpg" width="50%" alt="Image of the landing page."><br>
<img src="readmefiles/gamepage-image.jpg" width="50%" alt="Image of the game page."><br>
I've been using the responsive layout a lot in inspect mode using Google Chrome.

## <a id ="more-features"></a>More Features?

A couple of things is in my mind.
<ul>
<li> The ability to go to next level if you win a round of ten points. Just for fun. The game can't be "harder" on a higher level. :-D</li>
<li> Adding more codes for different features.</li>
</ul>

## <a id="testing"></a>Testing

I started to stuggle a bit with updating cells in google sheet.
I wanted the cells to update with one row of data:<br>
     ```character_data = [player_name, char_name, char_str, char_sta, char_cha] ```<br>
     ```player_sheet.update("A2:E2", [character_data]) ```

Event though it works the terminal gives me the following warning:<br>
    " ```/home/codeany/.local/lib/python3.8/site-packages/gspread/worksheet.py:1069: UserWarning: [Deprecated][in version 6.0.0]: method signature will change to: 'Worksheet.update(value = [[]], range_name=)' arguments 'range_name' and 'values' will swap, values will be mandatory of type: 'list(list(...))'
  warnings.warn(" ```

So I changed it to update each cell individually. Not pretty, I know, but couldn't find a way to get it working without a warning.<br>
     ```player_sheet.update_acell('A2', player_name)```<br>
     ```player_sheet.update_acell('B2', char_name)```<br>
     ```player_sheet.update_acell('C2', char_str)```<br>
     ```player_sheet.update_acell('D2', char_sta)```<br>
     ```player_sheet.update_acell('E2', char_cha)```<br>

In contrast to the first project. I continuously tested the code along to with coding to make sure everything is ok.

Some things that come up is to add a header to each section in the html code. But I later changed the sections and just had one header added.

The CSS Validator gave me two errors. One that I had forgot to write a unit on a margin. And the second one was that I had typed "position; bottom;"
which I changed to "position; fixed;".

I also used Lighthouse in Chrome to find ways to increase the accessibility of the website.<br>

Links to the validation
<ul>
<li> HTML of <a href="https://validator.w3.org/nu/?doc=https%3A%2F%2Frobertahlin.github.io%2Frps-project2b%2Findex.html" target="_blank">index</a> page.</li>
<li> HTML of <a href="https://validator.w3.org/nu/?doc=https%3A%2F%2Frobertahlin.github.io%2Frps-project2b%2Fgame.html" target="_blank">game</a> page.</li>
<li> CSS of <a href="https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Frobertahlin.github.io%2Frps-project2b%2Fassets%2Fcss%2Fstyle.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en" target="_blank">style.css</a>.</li>
<li> To validate my JavaScript I  used <a href="https://jshint.com/" target="_blank">https://jshint.com/</a>. (Couldn't find a way to post links, directly to the JavaScript file.)</li>
</ul>

Other than the validators. I've been using the Inspect view in Google Crome using different layout for different devices and a lot with the responsive layout.
I also tested the website through my iPhone.
I've tested the website on a PC using Chrome and Edge web browsers.
Also, my mentor has tried the website.

### <a id="bugs"></a>Bugs?

<ul>
<li>There is something with the "swap image function" when clicking the "Reset scores" button. Sometimes it doesn't swap to the "down button image". After hard refreshing the page a couple of times it works. Sometimes it works when holding down the mouse button for a while. It also seems to work better in Microsoft Edge.</li>
<li>Also the swap image function doesn't seem to respond when in inspect mode in Google Chrome.
<li>The toggle of div containing the instructions on the index page don't work when the script is in the script.js file. I had to place it in another file called index-script.js. I discovered that if I placed it first in the script.js document it worked, but then the swap image effect on the "Reset Score" button stopped working completely. I couldn't figure out why. So the solutions was to have them in different files.</li>
</ul>

## <a id="deployment"></a>Deployment


The site was deployed to Heroku. Using the Code institute guidence from Love Sandwiches walkthrough.
<ul>
<li>I used the GitHub template to create my own repository.</li>
<li>Used Codeanywhere as IDE.</li>
<li>Made a Google sheet and set up the API acording to the videos in the Love Sandwiches walkthrough.</li>
<li>I deployed the project to Heroku goint through these steps.</li>
    <ol>
    <li>Create new app</li>
    <li>Named it: rpg-p3 (Short for Role Playing Game - Project 3)</li>
    <li>Choosed Europe as region</li>
    <li>I went to the Settings tab to create config vars for CREDS and PORT</li>
    <li>I added the buildpacks Python and Nodejs</li>
    <li>In the Deploy tab I connected to GitHub repository "rpg-p3"</li>
    <li>I manually deployed branch (main)</li>
    <li></li>
    <li></li>
    </ol>
</ul>


## <a id="credits"></a>Credits

<ul>
<li>For this project I want to credit the Google search engine. It's hard to remember how to write all codes.</li>
<li>A lot of help comes from search hits at the "stack overflow" forums.</li>
<li>The game story written by ChatGPT with my instructions.
</ul>

### <a id="acknowledgements"></a>Acknowledgements

- My mentor, Medale Oluwafemi, for great suggestions and help and for showing how use document tags at <a href="https://jsdoc.app/about-getting-started.html" target="_blank">https://JSDoc.app</a>

# Virtual Try-On

What if I could try on outfits live? Whilst there are plenty of experiences which promise that, few offer a genuine real-time and interactive experience. My belief is that if a user is truly able to acutely visualise the look and feel of clothing, it would greatly increase their propensity to buy. And, no other experiences that I'm aware of can satisfy this criteria fluidly. I built this experiment with [Odyssey's](https://odyssey.ml/) real-time generative models to test virtual try-on. Try [here](https://odyssey-virtual-tryon.onrender.com/). In this demo, a user can drag and drop different preset clothing items onto the character which models them in real-time. The user can also prompt the model to change stance to help visualise the outfit from all angles as well as in motion e.g. walking. In the future, it should be possible to personalise further by using your own image, selecting your own clothing items and perform any actions.

[Note, the demo only works for the female model and is limited to one concurrent user by Odyssey. This will only last until I have API credits].

![image](./assets/documentation/landing_page.png)

### Reflections
Odyssey's it models are currently not capable enough for this application. The major issues are:

1. Too many hallucinations. There are many times when the model would distort the model, hallucinate additional people or simply fail to render the clothing properly e.g. one-sleeved jacket. I tested a variety of prompts but the issue appears to be a limitation of the current model.

2. Failure to follow instructions. Frustratingly, there were a number of times when the model would blatantly refuse to follow instruction e.g. change the colour of a piece of clothing or making the subject move according to the prompt's instruction. Repeating the instruction multiple times sometimes persuaded the model to obey but often even this fell on 'deaf' ears. 

3. Slow generation. Latency was a big issue. I had to often wait a couple of seconds before I saw the model begin changing the scene. This isn't an issue with the video stream but an issue with how quickly the model decides to respond to the changes. For an application like this, fast feedback is critical. Also, as mentioned above, I usually had to prompt the model multiple times and occasionally with some other action to trigger the new generations. 

4. Lacks visual stability. When it gets it right, it's incredible but often the image will distort and morph slowly out of shape.

In short, the models aren't ready for prime time but I'm optimistic about the potential. When it works, it's incredible and will afford all sorts of dynamic changes that can lend itself to a joyful experience. Forget an ordinary catwalk, you could simulate how an outfit would look like on a flowing dancer or sprinting athlete.

## How to Run Locally

### Prerequisites
- Python 3.x installed on your system

### Starting the Development Server

**Build the static site**
```bash
export ODYSSEY_API_KEY='your_api_key_here'
python3 build.py
```

**Start the Python HTTP server:**
```bash
cd public
python3 -m http.server 8000
```

**Open your browser and visit:**
```
http://localhost:8000
```

## Project Structure

- `index.html` - Main application file
- `clothing-config.json` - Clothing configuration
- `assets/` - Project assets

The `clothing-config.json` contains asset information which is loaded on the virtual try-on page. Update this and the assets to load a different configuration.

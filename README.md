# Virtual Try-On

An experiment with [Odyssey's](https://odyssey.ml/) real-time generative models to test a virtual try-on application for clothing visualization. Try [here](https://odyssey-virtual-tryon.onrender.com/). Note, the demo only works for the female model and is limited to one concurrent user by Odyssey. This will only last until I have API credits.

![image](./assets/documentation/landing_page.png)

## Reflections
My interest was to enable users to try on new outfits in real-time. There are plenty of similar experiences already available but few which offer a real-time interactive experience. So what? My thought was that it would drive increased likelihood to purchase if a consumer could more acutely visualise the item they're interested in. Other experiences are limited to images or generate a one-time video which limits the actions and settings which can be visualised.

### Lessons
Right now, Odyssey's models are not capable enough for this application. The major issues are:

1. The models hallucinate quite frequently. There many times when the model would paint multiple avatars in the frame or fail to fully depict the clothing e.g. one-sleeved jacket or distorting the subject's body. Arguably this is a prompting failure, but I think that's a stretch.

2. Failure to follow instructions. Frustratingly, there were a number of times when the model would blatantly refuse to follow instruction e.g. change the colour of a piece of clothing or making the subject move according to the prompt's instruction.

3. Slow generation. Latency was a big issue. I had to often wait a couple of seconds before I saw the model begin changing the scene. Usually, I had to prompt it with some other action to trigger the generations. In an experience like this, fast feedback is critical.

4. Consistency. When it gets it right, it's incredible but often the image will distort and morph slowly out of shape annoyingly.


In short, the models aren't ready for prime time but I'm optimistic about the potential. When it works it's incredible to have real-time transformation. It affords all sorts of dynamic changes that can lend itself to a joyful experience. Forget an ordinary catwalk, you could simulate how an outfit would look like on a flowing dancer or sprinting athlete.

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

# 🎡 Spinnit!

> having a tough time making decisions? spin me to see where your fate lies 💫

### Link to Spinnit!: https://t.me/spinnitbot

![demo](/assets/demo/demo.gif)

### Features
- Creates gif on the fly with user's options 🎨
- Special mode for special users only 💞
- Group-friendly 👥
- Cute pics 😍
- Free 🎉

### Usage 
1. Ensure you have Telegram installed on your device
2. Visit my bot link: https://t.me/spinnitbot
3. Enter /halp to see available commands

### Development
- Deployed on AWS
- As gifs are restricted to 256 colours, I had to remap the colours to reduce posterization using quantization
- Uses custom rate limiter that implements the token bucket algorithm while capping each unique and non-special user to at most 2 spins every 5 minute window period (Telegram imposes a rate limit of sending 10 gifs every 5 minutes 😿)

### Building your own Docker Image
To build a Docker image for Spinnit!, follow these steps:

1. Make sure you have Docker installed on your machine.

2. Clone the repository from GitHub:

   `git clone https://github.com/linustws/spinnit`
3. Navigate to the project's root directory:

   `cd spinnit`
4. Configure the environment variables in the Dockerfile. These variables are necessary for configuring the Spinnit bot. Open the Dockerfile and locate the following lines:

   ```
   ENV TELEGRAM_TOKEN='your telegram token'
   ENV DEVELOPER_CHAT_ID='your developer chat id'
   ENV SPECIAL_IDS='your special ids'
   ```
   
   Replace `'your telegram token'`, `'your developer chat id'`, and `'your special ids'` with your actual values.

   `your telegram token` -> `'<token from BotFather>'`
   
   `your developer chat_id` -> `'<your Telegram ID>'` (you can use this bot _@userinfobot_ to get your Telegram ID)
   
   `your special ids` -> `'<Telegram IDs that can use the special mode>'` (separated by spaces e.g. '123456789 987654321'). If you do not want to have a special mode feature, just leave this unchanged. _Note: Special mode requires you to provide **square pictures in the form of .png/.jpg/.jpeg** (unless you want stretched pictures) in the special folder (under `assets/images`), Spinnit! will use the general pictures if special pictures cannot be found._

5. Open a terminal or command prompt.
Build the Docker image by running the following command:

   `docker build -t spinnit:latest .`

   Wait for the build process to complete. This may take a few minutes, depending on your internet connection.
   Once the build is finished, you will have a Docker image with the tag spinnit:latest locally on your machine.
   Now you can use the spinnit:latest Docker image to run containers of your Spinnit application.

6. To run a container using the built image, execute the following command:

   `docker run -d -v spinnit:/app/spinnit/logs --name spinnit spinnit`

If you want your bot to run independently, you have to deploy it with a cloud service provider (e.g. AWS).

Feel free to customize the Dockerfile and docker run command as per your requirements.

Please let me know if you need any further assistance!
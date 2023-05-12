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

### Building the Docker Image
To build a Docker image for Spinnit!, follow these steps:

1. Make sure you have Docker installed on your machine.

2. Clone the repository from GitHub: 

    `git clone https://github.com/linustws/spinnit`
3. Navigate to the project's root directory:

   `cd spinnit`
4. Configure the environment variables in the Dockerfile. These variables are necessary for configuring the Spinnit bot. Open the Dockerfile and locate the following lines:

```
ENV TELEGRAM_TOKEN=your_telegram_token
ENV DEVELOPER_CHAT_ID=your_developer_chat_id
ENV SPECIAL_IDS=your_special_ids
```

Replace `your_telegram_token`, `your_developer_chat_id`, and `your_special_ids` with your actual values. These environment variables are used by the Spinnit bot to connect to Telegram and perform its functions. 




ENV TELEGRAM_TOKEN=your_telegram_token

Open a terminal or command prompt.
Build the Docker image by running the following command:
bash
Copy code
docker build -t spinnit:latest .
Wait for the build process to complete. This may take a few minutes, depending on your internet connection.
Once the build is finished, you will have a Docker image with the tag spinnit:latest locally on your machine.
Now you can use the spinnit:latest Docker image to run containers of your Spinnit application.

To run a container using the built image, execute the following command:

bash
Copy code
docker run -d -p 80:80 spinnit:latest
This command starts a new container in the background (-d flag) and maps port 80 of the container to port 80 of the host (-p 80:80 flag).

You can now access your Spinnit application by visiting http://localhost in your web browser.

Feel free to customize the Dockerfile and docker run command as per your requirements.

Please let me know if you need any further assistance!
# 🎡 Spinnit!

> having a tough time making decisions? spin me to see where your fate lies 💫

### Link to Spinnit!: https://t.me/spinnitbot

![demo](/Users/linustws/Desktop/Spinnit!/assets/demo/demo.gif)

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
- Deployed on aws
- As gifs are restricted to 256 colours, I had to remap the colours to reduce posterization using quantization
- Uses custom rate limiter that implements the token bucket algorithm while capping each unique and non-special user to at most 2 spins every 5 minute window period (Telegram imposes a rate limit of sending 10 gifs every 5 minutes 😿)
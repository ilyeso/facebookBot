
# Facebook Auto Liker & Commenter

This Flask application automates the process of liking and commenting on Facebook posts. It uses Selenium and a web driver to interact with Facebook, making it easy to engage with content without manual effort.


## Features :
* Automated interaction: Automatically likes and comments on a specified Facebook post.
* Customizable comments: Add personalized comments for each post.
* Secure credentials: Uses a credentials.json file to store your Facebook login information.
* Easy setup: Clear instructions for installation and usage.

## Installation

1- Clone the repository:

```bash
  git clone https://github.com/ilyeso/facebookBot.git

```
2- Install dependencies:

```bash
pip install -r requirements.txt
```
3- Web driver setup:

The code automatically download the latest version of ChromeDriver, but if you have any problem, just download the appropriate web driver from the official source and place it in your system's PATH or your project directory.

## Usage

1- Update credentials:

Open the credentials.json file and replace the placeholders with your Facebook bot's username and password:
```json
{
    "username": "your_bot_username",
    "password": "your_bot_password"
}
```
2- Run the application:

The app will launch at http://127.0.0.1:5000/ in your web browser.

3- Input post details:

Enter the URL of the Facebook post you want to target.
Type your desired comment in the provided field.
Click the "Submit" button.

4- Automatic interaction:

The bot will log into Facebook, navigate to the specified post, like it, and add your comment.

# Important Notes
- Ethical use: Please use this bot responsibly and respect Facebook's terms of service.
- Security: Keep your credentials.json file confidential.
- Dependencies: Ensure the required web driver is installed and accessible by the script.

# Disclaimer
This application is for educational and demonstrative purposes only. I am not responsible for any misuse or consequences arising from the use of this tool.



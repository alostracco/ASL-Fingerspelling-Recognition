# ASL Fingerspelling Recognition

For optimal compatibility, it is recommended to utilize Python Version 3.8

How to Set Up a Python Virtual Environment and Clone a Repository

Follow these steps to effectively clone a Git repository, create a Python virtual environment, and start working on your project:

## Step 1: Check for Git Installation

First, verify if Git is already installed on your system by running the following command:

```bash
git --version
```

If Git is not installed, you can download and install it from the official website: [Git Downloads](https://git-scm.com/downloads).

## Step 2: Clone the Git Repository

Clone the Git repository with the following command:

```bash
git clone https://github.com/alostracco/ASL-Fingerspelling-Recognition.git
```

## Step 3: Navigate to the Cloned Repository

Change your current directory to the cloned repository:

```bash
cd ASL-Fingerspelling-Recognition
```

## Step 4: Install `virtualenv`

To create isolated Python environments, you need to install the `virtualenv` package. Use the following command:

```bash
pip install virtualenv
```

## Step 5: Create a Virtual Environment

Set up a new virtual environment in a directory named 'venv' with this command:

```bash
python -m venv venv
```

## Step 6: Activate the Virtual Environment

Activate the virtual environment to isolate your Python environment and utilize the packages installed within it:

- On Windows:

```bash
. venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

## Step 7: Install Project Dependencies

Install the necessary packages listed in your `requirements.txt` file using the following command:

```bash
pip install -r requirements.txt
```

## Step 8: Open Your Project in Visual Studio Code

Launch Visual Studio Code in your project directory with the following command:

```bash
code .
```

## Step 9: Run Your Project

You are now ready to run your project using the appropriate commands or scripts.

## Acknowledgements

- [@grassknoted/aslalphabet_akash nagaraj_2018](https://www.kaggle.com/grassknoted/aslalphabet_akash%20nagaraj_2018)
- Title: ASL Alphabet
- URL: [https://www.kaggle.com/dsv/29550](https://www.kaggle.com/dsv/29550)
- DOI: 10.34740/KAGGLE/DSV/29550

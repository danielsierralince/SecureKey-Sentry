<a name="readme-top"></a>
<div align="center">
    <img src="password.ico" alt="logo" width="140" height="auto" />
    <br/>
    <h3><b>SECUREKEY SENTRY</h3>
</div>

**SecureKey Sentry** is an OTP (One Time Password) system that integrates graphical user interface, hash tables and connection to a database.

SecureKey implements security protocols for access control through a hashed dynamic key, while Sentry requests and verifies the OTP to authorize access to a banking system. Sentry evokes the image of a protective guardian tasked with system security.

The program utilizes a hash table data structure to store user data in the database. Each user is assigned a unique identifier generated through a combination of folding and quadratic probing techniques by working with the user identification card. These techniques facilitate rehashing for efficient collision handling.

## Built With <a name="built-with"></a>

1. Python. 
2. Tkinter. 
3. Hash tables. 
4. MongoDB. 

### Tech Stack <a name="tech-stack"></a>

<details>
    <summary>Client</summary>
    <ul>
        <li><a href="https://docs.python.org/es/3/library/tkinter.html">Tkinter</a></li>
    </ul>
</details>

<details>
    <summary>Server</summary>
    <ul>
        <li><a href="https://docs.python.org/es/3/">Python</a></li>
    </ul>
</details>

<details>
    <summary>Database</summary>
    <ul>
        <li><a href="https://www.mongodb.com/"></a>MongoDB</li>
    </ul>
</details>

## Getting Started <a name="getting-started"></a>

To get a local copy up and running, follow these steps.

### Prerequisites

In order to run this project you need:

- Python 3.11.2 64-bit
- MongoDB 6.0.5 2008R2Plus SSL (64 bit)
- MongoDB Compass v1.37.0

### Setup

Clone this repository to your desired folder and install packages required for the project and their versions. Run this command:

```sh
  cd my-folder
  git clone https://github.com/danielsierralince/SecureKey-Sentry.git
  pip install -r requirements.txt
```

Don't forget creating the database (mongodb://localhost:27017/) with name 'SecureKey-Sentry' and fill the collection 'Users' through empty_collection.py

### Usage

To run the project, open 'SecureKey.exe' and 'Sentry.exe', wich are included in the 'dist' folder.

## Authors <a name="authors"></a>

**Daniel Sierra Lince**
- GitHub: [@github](https://github.com/danielsierralince)
- Twitter: [@twitter](https://twitter.com/sierra_lince)
- LinkedIn: [@LinkedIn](https://www.linkedin.com/in/daniel-sierra-lince/)

## Future Features <a name="future-features"></a>

 - [ ] **...**

## Show your support <a name="support"></a>

If you like this project just give it a star 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

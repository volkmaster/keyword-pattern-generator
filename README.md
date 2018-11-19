# Word-Image-Collage
Word Image Collage (Brand New Coexistence Exhibition) application for constructing random documents filled with text and images and printing them out on multiple printers.
### Installation
##### Clone the git repository
`git clone https://github.com/volkmaster/word-image-collage.git`  
##### Download and install anaconda 3 from https://www.continuum.io/downloads
##### Install additional Python libraries:
`pip install python-dotenv`  
`conda install -c conda-forge google-api-python-client`  
`pip install python-twitter`  
`pip install wikipedia`  
`pip install unidecode`  
### Config and run
##### Config `.env` file
Copy `.env.example` to `.env` and fill out the listed parameters.
##### Run the program

- Generate a document based on 3 random keywords:

    `python runner.py`

- Generate a document based on 3 given keywords (GUI):
    
    `python ui.py`

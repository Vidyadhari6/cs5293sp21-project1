# cs5293sp21-project1

###redact_names(n_lines, input_files):

    It takes the text of the file and filename as input and it masks the words related to person names and returns the redacted names and unique number of names it has redacted.

###redact_dates(d_lines, input_files):

    It takes the text of the file and filename as input and it masks the dates and returns the updated text with the masked words and unique number of dates it has redacted.


###redact_phones(p_lines, input_files):

    It takes the text of the file and filename as input and it masks the phone numbers and returns the updated text with the masked words and unique number of phonenumbers it has redacted.



###redact_genders(g_lines, input_files):

    It takes the text of the file and filename as input and it masks the gender related to person names and returns the updated text with the masked words and number of gender it has redacted.

###redact_concept(c_lines, input_files, concept):

    It takes the text of the file, filename and concept word as input and it masks the entire sentence related to concept word and returns the updated text with the masked lines.

###write_output(output_dir, file, docs):

    It takes the name of the directory, filename and the resultant text. It creates the directory with same name as the original file with the extension .redacted and stores the masked text in it.

###args = stats

    It returns total number of names redacted in the file, total number of gender identifiers redacted in the file, total number of phone numbers redacted in the file, total number of dates redacted in the file in an output file with same name as the original file with the extension .stats

###steps to install required dependencies:
    1. Create a python virtual environment using pipenv
        a. pip install pipenv - installs pipenv package that is used to create python virtual environment
        b. To install any python dependency we have two options
            1. pipenv install <PACKAGE_NAME> - This will install any dependency in python virtual environment and creates 
               Pipfile, which will contain all required dependencies for our project
            2. If the project already contains Pipfile then to install all required dependencies for that project you can use
                the dependencies mentioned in the Pipfile using **pipenv run** command. This will install all required dependencies and 
                your python process.
        c. pipenv creates a Pipfile.lock file to maintain and lock python dependencies for that pipenv environment.
        d. To run a python process in pipenv virtual environment use **pipenv run** command.

###Running code
    
    1. git clone git@github.com:Vidyadhari6/cs5293sp21-project1.git
    2. cd cs5293sp21-project1/
    3. git checkout tags/v1.0
    4. pip install pipenv
    5. pipenv install
    6. pipenv run python3 project1/redactor.py --input 'project1/*.txt' --names --dates --phones --concept 'kids' --output 'files' --stats 'stats_out'


Running unit test
pipenv run pytest
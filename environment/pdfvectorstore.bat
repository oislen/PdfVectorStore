:: list all available conda environments
call conda env list

:: create and activate new environment
call conda env remove --name pdfvectorstore
call conda env list
call conda create --name pdfvectorstore python=3 --yes
call conda activate pdfvectorstore
call conda list

:: install all relevant python libraries
call pip install -r ..\requirements.txt

:: list all installed libraries
call conda list

:: export to yml file
:: call conda env export > pdfvectorstore.yml
:: call conda env create -f pdfvectorstore.yml

::call conda deactivate
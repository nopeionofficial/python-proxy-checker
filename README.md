# **Proxy Checker**
This is a simple script that checks the response time of a list of HTTP/HTTPS proxies and exports the working ones to a file.

## **Installation**
Before running the script, make sure to install the required dependencies:
```py
pip install -r requirements.txt
```
or run the "**install.bat**".

## **Usage**
To use Proxy Checker, you need to modify the settings in the "**config.json**" file. The settings are as follows:

- '**timeout**': Timeout for connecting to a proxy server (in seconds)

- '**max_ms**': Acceptable maximum response time (milliseconds)

- '**host**': URL to be used to check if the proxy is responding or not

- '**input**': List of proxies to be checked (can take multiple txt files)

- '**export**': Name of the file where successful proxies will be saved

- '**threads**': Specifies the number of threads that will be used to check the proxies simultaneously

then run the script by using this command:
```py
python proxy_checker.py
```
or run the "**start.bat**".


By default, the script reads the proxy list from the proxies.txt (includes others if any) file and exports the working proxies to the working_proxies.txt file.

You can also specify the maximum response time for a proxy to be saved by modifying the '**max_ms**' parameter in the "**config.json**" file.
This parameter, although it appears to do the same job as timeout, I did not remove it as it may be useful in some projects.

## **Contributing**
If you find any bugs or have suggestions for improvements, please open an issue or pull request on this repository.

## **License**
This project is licensed under the __MIT License__.


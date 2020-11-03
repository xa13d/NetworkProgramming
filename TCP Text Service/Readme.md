
# Lab2 - Text Service - Python Network Programming


## Description

It is console app. We can send two types of modes from client terminal to the server: Change text and Encoder/Decoder

## Requirements

- Python3
- Windows/\Unix OS

## Installation

```
git clone https://github.com/xa13d/NetworkProgramming.git
cd "TCP Text Service"
pip install -r requirements.txt
```

## Usage

**Options** for the program:

```
-h, --help			Help Menu
--host				Destination IP Address
-m					Client working mode
-p 					Destination Port
-f 					File
-a 					Additional file
```


**Server** mode:

```
python3 TextService.py server -p <PORT>
```

**Client** mode:

```
python3 text_service_TCP.py client -h <DST-IP> -p <PORT> -m <MODE> -f <FILE> -a <ADDITIONAL>
```

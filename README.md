# CanEdge1 Data Converter

This tool is used to convert .MF4 to .csv. Split data by CANID.

![CANEdge1](https://canlogger.csselectronics.com/canedge-docs/ce1/_images/canedge1.jpg)

# Develop Environment
Python3

## Dependency
```
pip install python-can-csscan-mf4
pip install python-can==4.3.1
pip install bitstring==4.2.3
```

# Application

```
python main.py data/00000001.MF4
```

Output files:<br/>
can_0x01000001.csv<br/>
can_0x01000002.csv<br/>
can_0x01000003.csv<br/>
can_0x01000004.csv

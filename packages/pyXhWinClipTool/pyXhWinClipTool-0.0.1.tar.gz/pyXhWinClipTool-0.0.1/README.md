# PyXhWinClipTool

# Installation
```python_script
pip install pyXhWinClipTool -U

# Or

pip3 install pyXhWinClipTool -U
```

# Demo
```shell
# Help
python -m pyXhWinClipTool --help

# Copy to clipboard
echo "msg" | python -m pyXhWinClipTool --copy 
# Or
echo "msg" | python -m pyXhWinClipTool -c 

# Retrieve data from clipboard
python -m pyXhWinClipTool --paste 
# Or
python -m pyXhWinClipTool -p
```

# Source Description
The pyXhWinClipTool is simple. It is just a wrapper to windows existing command for operate with clipboard.

## Copy
In windows, we could use command 'clip' to copy text to clipboard.
e.g.
```
echo "hihi" | clip
```

## Paste
In windows, we could use command 'powershell' to retrieve text from clipboard.
e.g.
```
powershell get-clipboard
```

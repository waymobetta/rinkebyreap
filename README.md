# rinkebyreap

### requirements

1. Obtain API credentials for:
	- Twitter (https://apps.twitter.com)
	- Etherscan (https://etherscan.io/login?cmd=last)

2. Add API credentials to `.bashrc` or `.env`

3. Copy wallet address for testnet Ether

4. Install required packages
```bash
[sudo] pip install -r requirements.txt
```

### usage

Run usage/help
```bash
./reaper.py -h
```

Run and delete tweet
```bash
./reaper.py -d
```

Run as phantom browser and delete tweet
```bash
./reaper -p -d
```

### notes
- Developed and tested on MacOS
- Currently requests max amount of Ether (18.75/3 days)
- Needs proper error handling

MIT

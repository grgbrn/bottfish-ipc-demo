## setup

Create the named pipes from the shell:

```
mkfifo n2p
mkfifo p2n
```

send a network message to the node process:

```
curl -d "@input.json" -X POST http://localhost:3000/data
```

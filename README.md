# Cache-simulator

The goal of this project is to help understand the internal operations of CPU caches. It simulates a Level 1 cache for a 32-bit CPU. Assume a 32-bit data bus. The cache must be command line configurable to be direct-mapped, 2-way, 4-way, 8-way, or 16-way set associative and implement both round- robin and random replacement policies for performance comparisons. You may implement LRU in lieu of either of the others.

### Flags:
```
–f <trace file name>    [ name of text file with the trace ]
–s <cachesizeinKB>      [1KB to 8MB]
–b <block size>         [ 4 bytes to 64 bytes ]
–a <associativity>      [ 1, 2, 4, 8, 16 ]
–r <replacement policy> [ RR or RND or LRU ]
```

### Example usage:
``` 
Sim.exe –f trace1.txt –s 1024 –b 16 –a 2 –r RR
```


## Outputs: 
```
Cmd Line: Reprint the command line used and the parsed parameters: Trace File: <name of trace file>
Cache Size: <size typed in KB>
Block Size: <size typed in bytes>
Associativity: <direct, 2-way, 4-way, etc.> R-Policy: <characters typed in>
```



### Example Output:

```
Example:
Cache Size: 1024 KB
Block Size: 16 bytes Associativity: 2 Policy: RR
```






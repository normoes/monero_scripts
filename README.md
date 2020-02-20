# Monero scripts

Get [Monero project](https://github.com/monero-project/) meta information.

These tools extract information from parts of the [Monero project](https://github.com/monero-project/) source code files.

## get_monero_hard_fork_info.py

Gets past hard fork dates, versions and information.

Goal:
  * Get monero hard fork dates from `/src/hardforks/hardforks.cpp`.

How to:
  * for default values and how to use the tool
    - `python get_monero_hard_fork_info.py --help`
  * current master:
    - `python get_monero_hard_fork_info.py`
    - `python get_monero_hard_fork_info.py --branch master`
  * It is also possible to set the branch name as environment variable: `PROJECT_BRANCH_NAME`.
    - `PROJECT_BRANCH_NAME=master python get_monero_hard_fork_info.py`
  * `python get_monero_hard_fork_info.py --branch release-v0.11.0.0`
    ```
        version 1 ['Apr 18 2014 UTC', '1', '1341378000']
        version 2 ['Mar 20 2016 UTC', '1009827', '1442763710']
        version 3 ['Sep 24 2016 UTC', '1141317', '1458558528']
        version 4 ['Jan 05 2017 UTC', '1220516', '1483574400']
        version 5 ['Apr 15 2017 UTC', '1288616', '1489520158']
        version 6 ['Sep 16 2017 UTC', '1400000', '1503046577']
    ```
  * `python get_monero_hard_fork_info.py --branch release-v0.12`
    ```
        ...
        version 7 ['Apr 06 2018 UTC', '1546000', '1521303150']
    ```
  * `python get_monero_hard_fork_info.py --branch release-v0.13`
    ```
        ...
        version 8 ['Oct 18 2018 UTC', '1685555', '1535889547']
        version 9 ['Oct 19 2018 UTC', '1686275', '1535889548']
        version 10 ['Mar 09 2019 UTC', '1788000', '1549792439']
        version 11 ['Mar 10 2019 UTC', '1788720', '1550225678']
    ```
  * It is possible to select the Monero network (`mainnet`, `testnet`, `stagenet`)
    - `python get_monero_hard_fork_info.py --network stagenet`
  * It is possible to select a different Monero daemon
    - `python get_monero_hard_fork_info.py --daemon localhost`

### Result without working daemon connection
In case the daemon shuold not be reachable (e.g. timeout, connection error, etc.), the result will be missing the date information:
```
Version 1 ['---', '1', '1341378000']
Version 2 ['---', '1009827', '1442763710']
Version 3 ['---', '1141317', '1458558528']
Version 4 ['---', '1220516', '1483574400']
Version 5 ['---', '1288616', '1489520158']
Version 6 ['---', '1400000', '1503046577']
Version 7 ['---', '1546000', '1521303150']
Version 8 ['---', '1685555', '1535889547']
Version 9 ['---', '1686275', '1535889548']
Version 10 ['---', '1788000', '1549792439']
Version 11 ['---', '1788720', '1550225678']
Version 12 ['---', '1978433', '1571419280']
```

## get_monero_seed_nodes.py

Gets Monero seed node IPs.

Goal:
  * Get monero seed nodes from `/src/p2p/net_node.inl`.

How to:
  * for default values and how to use the tool
    - `python get_monero_seed_nodes.py --help`
  * current master:
    - `python get_monero_seed_nodes.py`
    - `python get_monero_seed_nodes.py --branch master`
  * It is also possible to set the branch name as environment variable: `PROJECT_BRANCH_NAME`.
    - `PROJECT_BRANCH_NAME=master python get_monero_seed_nods.py`
  * `python get_monero_seed_nodes.py --branch release-v0.11.0.0`
    ```
        testnet ['212.83.175.67:28080', '5.9.100.248:28080', '163.172.182.165:28080', '195.154.123.123:28080', '212.83.172.165:28080', '195.154.123.123:28080', '212.83.172.165:28080']
        mainnet ['107.152.130.98:18080', '212.83.175.67:18080', '5.9.100.248:18080', '163.172.182.165:18080', '161.67.132.39:18080', '198.74.231.92:18080']
    ```
  * `python get_monero_seed_nodes.py --branch release-v0.15`
    ```
        testnet ['212.83.175.67:28080', '5.9.100.248:28080', '163.172.182.165:28080', '195.154.123.123:28080', '212.83.172.165:28080', '192.110.160.146:28080']
        stagenet ['162.210.173.150:38080', '162.210.173.151:38080', '192.110.160.146:38080']
        mainnet ['107.152.130.98:18080', '212.83.175.67:18080', '5.9.100.248:18080', '163.172.182.165:18080', '161.67.132.39:18080', '198.74.231.92:18080', '195.154.123.123:18080', '212.83.172.165:18080', '192.110.160.146:18080']
    ```
  * It is possible to select the Monero network (`mainnet`, `testnet`, `stagenet`)
    - `python get_monero_seed_nodes.py --network stagenet`

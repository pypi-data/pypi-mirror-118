# SIGMATMPY

> SIGMATMPY-library is an APIRequest driven trading and monitoring platform. Each functionality (trades, price etc.) is represented by it's own class covering all aspect of that functionality.


## Getting Started

### Installation

```sh
$ pip install sigmatmpy
```

### Basic functions

```sh
import sigmatmpy

# initualize APIRequest token
username = 'username'
password = 'password'
API = sigmatmpy.API(username,password)

# open a live order
API.open_order('EURUSD-R', 1, 0.01, 1.18245, 3, 0, 0,'comment')

# open a pending order (limit and stop order)
API.open_order('EURUSD-R', 3, 0.01, 1.18245, 3, 0, 0,'comment')

# modify a order
API.modify_order(2313839, 1.18245, 1.1825, 1.1824, 0)

# check if open order succeed
result = API.open_order('EURUSD', 1, 0.01, 1.18245, 3, 0, 0,'comment')
if result['code'] == 0:
    # successful
    continue
else:
    # unsuccessful
    continue

# close a live order 
API.close_order(9999999, 0.01, 1.18245)

# delete a pending order 
API.close_order(9999999)

# get trades history by datetime 
API.trades_history_by_datetime('2021-07-04 000000', '2021-07-16 075150')

# get trades history by unixtime 
API.trades_history_by_unixtime(1625991769, 1626423769)

# get live trades
API.live_trades()

# get account information
API.account_info()

# get server time
API.server_time()
```

### Price data

```sh
# initialize data streaming for XAUUSD
API.initialize_price_stream('XAUUSD')

# get current price
API.current_price('XAUUSD')

# get XAUUSD 5 min bar chart data
API.bar_chart('XAUUSD', 5)

# check appearance of new bar
API.check_new_bar('XAUUSD', 5)

```

## Error Code 

| Code | Description                                    |
|------|------------------------------------------------|
| 129  | Invalid price.                                 |
| 130  | Invalid stops.                                 |
| 131  | Invalid trade volume.                          |
| 134  | Not enough money.                              |
| 151  | The order you close is not under your account. |
| 153  | The symbol of order you placed is invalid.     |


## Authors 

* **SIGMATM** - *Initial work* - [SIGMATM]

Please read [contributors](#) for more information.

## License

Please read [LICENSE.md](LICENSE.md) for more detail.
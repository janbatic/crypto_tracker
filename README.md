# crypto_tracker

## APIS's

### Register
#### Request
> <span style="color:orange;"><strong>[POST]</strong></span> /api/user/register/

| Body parameter     | Type | Description                                                     |
|--------------------|------|-----------------------------------------------------------------|
| **username**       | str  | **Required.** Username of user that has to be unique            |
| **email**          | str  | **Required.** Email of user that has to be unique               |
| **password**       | str  | **Required.** Password of a user                                |
| **password_again** | str  | **Required.**  Password again that must be the same as password |

#### Response
 Status code 200, 400

 | Parameter  | Type | Description            |
|------------|------|------------------------|
| **Bearer** | str  | Users token to sign in |

### Login
#### Request
> <span style="color:orange;"><strong>[POST]</strong></span> /api/user/login/

| Body parameter | type | description                   |
|----------------|------|-------------------------------|
| **username**   | str  | **Required.** Users username. |
| **password**   | str  | **Required.** Users password. |

#### Response
 Status code 200, 400

 | Parameter  | Type | Description             |
|------------|------|-------------------------|
| **Bearer** | str  |  Users token to sign in |


### Logout
#### Request
> <span style="color:orange;"><strong>[POST]</strong></span> /api/user/logout/

 | Header parameter | Type | Description                          |
|------------------|------|--------------------------------------|
| **Bearer**       | str  | **Required.** Users token to sign in |
#### Response
 Status code 200, 401

### Transaction

#### Request
> <span style="color:orange;"><strong>[POST]</strong></span> /api/portfolio/transaction/

 | Header parameter | Type | Description                          |
|------------------|------|--------------------------------------|
| **Bearer**       | str  | **Required.** Users token to sign in |

| Body parameter       | Type  | Description                                                 |
|----------------------|-------|-------------------------------------------------------------|
| **cryptocurrency**   | str   | **Required.** Cryptocurrency that you wish to buy/sell      |
| **amount**           | float | **Required.** Amount you want to buy/sell                   |
| **transaction_type** | str   | **Required.** Transaction type that must be "buy" or "sell" |

#### Response
Status code 200, 400, 401

### Possession
#### Request
> <span style="color:green;"><strong>[GET]</strong></span> /api/portfolio/possession

 | Header parameter | Type | Description                          |
|------------------|------|--------------------------------------|
| **Bearer**       | str  | **Required.** Users token to sign in |

#### Response
| Parameter                   | Type  | Description                                        |
|-----------------------------|-------|----------------------------------------------------|
| **cryptocurrencies**        | list  | List of all crypto and their amounts in possession |
| **current_portfolio_value** | float | Current value of users portfolio                   |


### Crypto-info
#### Request
> <span style="color:green;"><strong>[GET]</strong></span> /api/crypto-info

 | Parameter | Type | Description    |
|-----------|------|----------------|
| **Page**  | num  | Number of page |

#### Response
| Parameter       | Type | Description                 |
|-----------------|------|-----------------------------|
| **crypto_info** | list | List of 25 cryptocurrencies |
| **page**        | int  | Page given                  |
| **num_pages**   | int  | Number of all pages         |

| crypto_info    | Type | Description            |
|----------------|------|------------------------|
| **name**       | str  | Name of cryptocurrency |
| **value**      | int  | Page given             |
| **market_cap** | int  | Number of all pages    |
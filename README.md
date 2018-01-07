# Crypto Summaries

If you automate crypto currency trading, and send out reports, you might want a summary of what a coin does, is it a coin that's for advertising? Gaming? Paying coffee?

This project tries to provide the simplest possible API to get a summary of a coin. Summaries come from [coinmarketcap](https://coinmarketcap.com/) and [cryptocompare](cryptocompare.com)

Check out [krausefx.github.io/crypto-summaries](https://krausefx.github.io/crypto-summaries/) for a list of the available summaries.

## State of the project

This is a super early version of what this might look like, of course there is not a ton of content here yet. Feel free to check out the existing, supported coins on [krausefx.github.io/crypto-summaries](https://krausefx.github.io/crypto-summaries/) and [contribute more on GitHub directly](#how-can-i-contribute).

## How to use the API

### Access the summary of Bitcoin:

- **1 line summary**: [https://krausefx.github.io/crypto-summaries/coins/btc-1.txt](https://krausefx.github.io/crypto-summaries/coins/btc-1.txt)
- **3 lines summary**: [https://krausefx.github.io/crypto-summaries/coins/btc-3.txt](https://krausefx.github.io/crypto-summaries/coins/btc-3.txt)
- **5 lines summary**: [https://krausefx.github.io/crypto-summaries/coins/btc-5.txt](https://krausefx.github.io/crypto-summaries/coins/btc-5.txt)

Alternatively you can also use the name of the coin instead of `symbol`

- **3 lines summary**: [https://krausefx.github.io/crypto-summaries/coins/bitcoin-3.txt](https://krausefx.github.io/crypto-summaries/coins/bitcoin-3.txt)

Note that the name/symbol always has to be lower case.

### Access the summary of Ethereum

Same thing, e.g.

- [https://krausefx.github.io/crypto-summaries/coins/eth-5.txt](https://krausefx.github.io/crypto-summaries/coins/eth-5.txt)
- [https://krausefx.github.io/crypto-summaries/coins/ethereum-1.txt](https://krausefx.github.io/crypto-summaries/coins/ethereum-1.txt)

## How does it work?

There is a reference folder called [./reference](./reference), that contains the summary for `x` sentences for each currency. Those will be copied over to the public facing `coins` directory with different names, to make the API as flexible as possible.

Check out the [./reference](./reference) directory, you can use the official `symbol` with the number of sentences (`[symbol]-[sentences].txt`) and store the summary in there. Next time the script runs, it will be applied to all the public facing `.txt` files.

If you want to help, check out [./missing_summaries.txt](./missing_summaries.txt) for the currencies for which there is no summary available at all.

## How can I contribute?

**Important**: Please only manually modify the files in the [./reference](./reference) directory, not the ones in `coins`, as those are the auto-generated ones.

You can use the GitHub UI to instantly edit the description without any coding skills:

- Press `t`
- Enter `reference/[coin_name]-[lines].txt`
- Press enter
- Press `e`
- Edit the content and hit the `Commit changes` button at the bottom of the page

## Re-generate the files

- Make sure to run `bundle install` to install all dependencies
- Run `bundle exec rake generate`
- Commit & push the changes

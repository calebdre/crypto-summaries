require_relative "./coinmarketcap"
require 'fileutils'

task :generate do
  coins_dir = "coins"
  FileUtils.mkdir_p(coins_dir)
  recorded_coins = Hash.new
  lengths = [1, 2, 3, 4, 5]
  all_coins = Coinmarketcap.fetch
  
  all_coins.each_with_index do |current_coin, index|
    next if index > 100
    output_names = [current_coin["name"], current_coin["id"], current_coin["symbol"]]


    lengths.each do |number_of_sentences|
      local_reference_path = File.join("reference", "#{current_coin['symbol']}-#{number_of_sentences}.txt")

      if File.exist?(local_reference_path)
        puts "Using local reference description of the coin #{current_coin['symbol']} for #{number_of_sentences} sentence(s)"
	
        all_sentences_file = File.join(coins_dir, "#{current_coin['symbol']}.txt".downcase)
        File.open("#{all_sentences_file}", "a+") { |f| f.write("#{File.read(local_reference_path)}\n") }

        output_names.each do |output_name|
          output_file = File.join(coins_dir, "#{output_name}-#{number_of_sentences}.txt".gsub("/", "-").downcase)
          FileUtils.cp(local_reference_path, output_file)
        end
        if not recorded_coins.has_key?(current_coin["symbol"])
          recorded_coins[current_coin["symbol"]] = [number_of_sentences]
        else
          recorded_coins[current_coin["symbol"]].push(number_of_sentences)
        end
      end
    end
  end

  all_coins_symbols = all_coins.map{|coin| coin["symbol"]}
  recorded_coins_symbols = recorded_coins.keys
  missing_summaries = all_coins_symbols - recorded_coins_symbols

  # Create an index.html
  html_content = ["<h1>An API for short summary of key features of all crypto currency</h1>"]
  html_content << "<ul>"
  html_content += recorded_coins.keys.uniq.collect do |current_symbol|
    "<li> #{current_symbol} (" + recorded_coins[current_symbol].collect do |number_of_sentences|
      link = File.join(coins_dir, "#{current_symbol}-#{number_of_sentences}.txt").downcase
      "<a href='#{link}' target='_blank'>#{number_of_sentences}</a>"
    end.join(", ") + ") <a href='#{File.join(coins_dir, "#{current_symbol}.txt").downcase}' target='_blank'>all</a></li>"
  end
  html_content << "</ul>"
  html_content << "<h3><a href='https://github.com/KrauseFx/crypto-summaries/'>Pull Requests welcome</a><h3>"
  html_content << "<h5>Webdesign and development by <a href='https://krausefx.com'>Felix Krause</a><h5>"
  puts html_content
  File.write("index.html", html_content.join("\n"))
  File.write("missing_summaries.txt", missing_summaries.uniq.join("\n"))
end

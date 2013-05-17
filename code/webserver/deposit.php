<?php
// This deposit.php requires that an empty file named "latest" is already created 
//  in the same directory.

ob_start();
$file = "latest";

// First, get the previous price values:
$prevPriceData = file_get_contents($file);
$prevPriceArr = explode("\n", $prevPriceData);

$currentTime = time();
//$currentPriceData = "";
foreach($prevPriceArr as $entry)
{
	$arr = explode(":", $entry);
	$time = $arr[0];
	$price = $arr[1];

	if($currentTime-$time < 20)
	{
		$currentPriceData .= $time.":".$price."\n";
	}
} 

// Get the latest MtGox value for $0.50 USD
$string = file_get_contents("http://data.mtgox.com/api/1/BTCUSD/ticker");
$result = json_decode($string);
$amount = .5/($result->return->last->value);

// Add the latest price to the list
$latestEntry = $currentTime . ":" . $amount;
$currentPriceData .= $latestEntry;

file_put_contents($file, $currentPriceData);

// Clear out the output buffer
while (ob_get_status()) 
{
	ob_end_clean();
}
header("Location: bitcoin:1MWMhhQiQQEPv4F8uJrFgi6rN9rZa6TJ5?amount={$amount}");

exit;

?>
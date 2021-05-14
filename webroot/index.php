<?php

$BOARD_SIZE = 9;
$board  = array();
$NO_VALUE= 0;


function solve_sudo($board) {
	global $NO_VALUE, $board, $BOARD_SIZE;
	$BOARD_START_INDEX = find_next($board); //<---array(1,2)
	// check if the board finish
	if ($BOARD_START_INDEX[0] == -1){
		return true;
	}
    for ($row = $BOARD_START_INDEX[0]; $row < $BOARD_SIZE; $row++) {
        for ($column = $BOARD_START_INDEX[1]; $column < $BOARD_SIZE; $column++) {
            if ($board[$row][$column] == $NO_VALUE) {
                for ($k = $MIN_VALUE; $k <= $MAX_VALUE; $k++) {
                    $board[$row][$column] = $k;
                    if (isOkay($board, $row, $column) && solve_sudo($board)) {
                        return true;
                    }
                    $board[$row][$column] = $NO_VALUE;
                }
                return false;
            }
        }
    }
    return true;
}

function isOkay($board,$num, $row, $col) {
  for ($i = 0 ;$i<9;$i++)
    if ($board[$i][$col] == $num) {
      return false;
    }
  for ($j = 0 ;$j<9;$j++)
    if ($board[$row][$i]== $num) {
      return false;
    }
  $r = $row - $row % 3;
  $c = $col - $col % 3;
  
  for ($i = $r; $i < $r + 3; $i++)
    for ($j =$c; $j < $c + 3; $j++)
      if ($board[$i][$j] == $num)
        return false;
    
  return true;
}

function find_next($board){
	global $NO_VALUE;
	for($i = 0 ;$i<9;$i++)
        for ($j = 0 ;$j<9;$j++)
            if ($board[$i][$j]==$NO_VALUE){
                return array($i,$j);
            }
                
    return array(-1,-1);
}
    

// Rest POST, GET
echo $_POST["board"];
//get the jason project to array.
$board = json_decode($_POST["board"],true);
$question = $board;
//forward file toward.
echo json_encode($board);

$data = array(
    'question' => json_encode($question),
    'solution' => json_encode($board)
);
# Create a connection
$url = 'http://localhost:7652';
$ch = curl_init($url);
# Form data string
$postString = http_build_query($data, '', '&');
# Setting our options
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
# Get the response
$response = curl_exec($ch);
curl_close($ch);

$list = array (
$question,$board
);
$file = fopen("sample.csv","w");
foreach ($list as $line) {
  fputcsv($file, $line);
}
fclose($file);

/*
in: 2darray 
out: 2darray
*/
?>
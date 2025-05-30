<?php

  session_start();

  $filename = 'shc_log_'.date('Y-m-d').'.txt';
  $file  = '../Logs/'.$filename;

  //$total_lines = shell_exec('cat ' . escapeshellarg($file) . ' | wc -l');

  //if(isset($_SESSION['current_line']) && $_SESSION['current_line'] < $total_lines){

  //  $lines = shell_exec('tail -n' . ($total_lines - $_SESSION['current_line']) . ' ' . escapeshellarg($file));

  //} else if(!isset($_SESSION['current_line'])){

    $lines = shell_exec('tail -n100 ' . escapeshellarg($file));

  //}

  //$_SESSION['current_line'] = $total_lines;
  
  $pattern = '/\/home\/data\/eumetcast\//';
  $replacement = ' ';
  $lines = preg_replace($pattern, $replacement, $lines);
  
  $pattern = '/\n\n/';
  $replacement = '---';
 
  $lines_replace = preg_replace($pattern, $replacement, $lines);

  $lines_array = array_filter(preg_split('/---/', $lines_replace));
  //$lines_array = array_filter(preg_split('#[\r\n]+#', $lines_replace));

  if(count($lines_array)){
    echo json_encode($lines_array);
  }

  ?>
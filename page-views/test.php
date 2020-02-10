
<html>
<head>
  <title>Page Views</title>
</head>
<body>
<?php
if(!file_exists('counter.txt')){
  file_put_contents('counter.txt', '0');
}
if($_GET['click'] == 'yes'){
  file_put_contents('counter.txt', ((int) file_get_contents('counter.txt')) + 1);
  header('Location: ' . $_SERVER['SCRIPT_NAME']);
  die;
}
?>
  <h1><?php echo file_get_contents('counter.txt'); ?></h1>
  <a href="?click=yes">clickMe</a>
</body>
</html>

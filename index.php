<!DOCTYPE html>
<html>
<head>
<style>
body {
 background-image: url("background.jpg");
 background-color: #ffffff;
} 
  
.button {
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 18px;
  margin: 4px 2px;
  cursor: pointer;
}

.button1 {background-color: #4CAF50;} /* Green */
.button2 {background-color: #008CBA;} /* Blue */
</style>
</head>
<body>
<h1>Pedometer</h1>
<p>Üdvözlünk újra az oldalon!</p>

<p>
<?php
$servername = "localhost";
$username = "admin";
$password = "raspberry";
$dbname = "pedometer";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM WalkingSession";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "id: " . $row["ID"]. " - CountOfSteps: " . $row["CountOfSteps"]. " Calories: " . $row["Calories"]. "<br>";
  }
} else {
  echo "0 results";
}
$conn->close();
?>

</p>

<button class="button button1">Legutolsó aktivitás</button>
<button class="button button2">Blue</button>

</body>
</html>

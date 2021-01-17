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

.button1 {background-color: #00A170;}
.button2 {background-color: #0072B5;}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #FFFFFF;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #A0DAA9;
}

tr:nth-child(odd) {
  background-color: #E9897E;
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

if(array_key_exists('button1', $_POST)) { 
    button1();
} 
else if(array_key_exists('button2', $_POST)) { 
    button2(); 
} 
function button1() { 
  global $conn;
  $sql = "SELECT ID, CountOfSteps, round(Calories,3) AS Calories FROM WalkingSession ORDER BY StopTime DESC LIMIT 1";
  $result = $conn->query($sql);
  
  if ($result->num_rows > 0) {
    echo "<table>";
    echo "  <tr>";
    echo "    <th>ID</th>";
    echo "    <th>Lépésszám</th>";
    echo "    <th>Kalóriamennyiség</th>";
    echo "  </tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
      echo "  <tr>";
      echo "    <td>" . $row["ID"] . "</td>";
      echo "    <td>" . $row["CountOfSteps"] . "</td>";
      echo "    <td>" . $row["Calories"] . " kcal</td>";
      echo "  </tr>";
    }
    echo "</table>";
  } else {
    echo "0 results";
  } 
    
} 
function button2() {
  global $conn;
  $sql = "SELECT ID, CountOfSteps, round(Calories,3) AS Calories FROM WalkingSession";
  $result = $conn->query($sql);
  
  if ($result->num_rows > 0) {
    echo "<table>";
    echo "  <tr>";
    echo "    <th>ID</th>";
    echo "    <th>Lépésszám</th>";
    echo "    <th>Kalóriamennyiség</th>";
    echo "  </tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
      echo "  <tr>";
      echo "    <td>" . $row["ID"] . "</td>";
      echo "    <td>" . $row["CountOfSteps"] . "</td>";
      echo "    <td>" . $row["Calories"] . " kcal</td>";
      echo "  </tr>";
    }
    echo "</table>";
  } else {
    echo "0 results";
  } 
} 

$conn->close();
?>

</p>

<form method="post"> 
<button type="submit" name="button1" class="button button1">Legutolsó aktivitás</button>
<button type="submit" name="button2" class="button button2">Összes aktivitás</button>
</form> 

</body>
</html>

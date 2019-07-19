<?php
require_once('db_connect.php');

session_start();
$tables = ['user', 'new'];


if (isset($_GET['t'])) {
    $type = mb_strtolower($_GET['t']);
    try {
        if ($type == 'sql') {
            Export_Database_SQL($host, $db_user, $db_pass, $db_name);
        } elseif ($type == 'csv') {
            Export_Database_CSV($host, $db_user, $db_pass, $db_name);
        } else {
            $_SESSION['msg'] = "No such type.";
            header('location: export.php');
        }
    } catch (Exception $e) {
        $_SESSION['msg'] = "DB error.";
        header('location: export.php');
    }
} else {
    $_SESSION['msg'] = "No such type.";
    header('location: export.php');
}


function Export_Database_SQL($host, $user, $pass, $name, $tables = false, $backup_name = false)
{
    $mysqli = new mysqli($host, $user, $pass, $name);
    $mysqli->select_db($name);
    $mysqli->query("SET NAMES 'utf8'");

    $queryTables = $mysqli->query('SHOW TABLES');
    while ($row = $queryTables->fetch_row()) {
        $target_tables[] = $row[0];
    }
    if ($tables !== false) {
        $target_tables = array_intersect($target_tables, $tables);
    }
    foreach ($target_tables as $table) {
        $result = $mysqli->query('SELECT * FROM ' . $table);
        $fields_amount = $result->field_count;
        $rows_num = $mysqli->affected_rows;
        $res = $mysqli->query('SHOW CREATE TABLE ' . $table);
        $TableMLine = $res->fetch_row();
        $content = (!isset($content) ? '' : $content) . "\n\n" . $TableMLine[1] . ";\n\n";

        for ($i = 0, $st_counter = 0; $i < $fields_amount; $i++, $st_counter = 0) {
            while ($row = $result->fetch_row()) { //when started (and every after 100 command cycle):
                if ($st_counter % 100 == 0 || $st_counter == 0) {
                    $content .= "\nINSERT INTO " . $table . " VALUES";
                }
                $content .= "\n(";
                for ($j = 0; $j < $fields_amount; $j++) {
                    $row[$j] = str_replace("\n", "\\n", addslashes($row[$j]));
                    if (isset($row[$j])) {
                        $content .= '"' . $row[$j] . '"';
                    } else {
                        $content .= '""';
                    }
                    if ($j < ($fields_amount - 1)) {
                        $content .= ',';
                    }
                }
                $content .= ")";

                if ((($st_counter + 1) % 100 == 0 && $st_counter != 0) || $st_counter + 1 == $rows_num) {
                    $content .= ";";
                } else {
                    $content .= ",";
                }
                $st_counter = $st_counter + 1;
            }
        }
        $content .= "\n\n\n";
    }
    $file_name = $backup_name ? 'backup.csv' : $name . "_" . date('H-i-s') . "_" . date('d-m-Y') . "_rand_" . rand(1, 11111111) . ".sql";
//    $backup_name = $backup_name ? $backup_name : $name . ".sql";
    header('Content-Type: application/octet-stream');
    header("Content-Transfer-Encoding: Binary");
    header("Content-disposition: attachment; filename=\"" . $file_name . "\"");
    echo $content;
    exit;
}


function Export_Database_CSV($host, $user, $pass, $name, $tables = false, $backup_name = false)
{
    global $pdo;

    $file_name = $backup_name ? 'backup.csv' : $name . "_" . date('H-i-s') . "_" . date('d-m-Y') . "_rand_" . rand(1, 11111111) . ".csv";

    $stmt = $pdo->prepare('SHOW TABLES');
    $stmt->execute();
    $result = $stmt->fetchAll(PDO:: FETCH_NUM);

    foreach ($result as $row) {
        $target_tables[] = $row[0];
    }
    if ($tables !== false) {
        $target_tables = array_intersect($target_tables, $tables);
    }

    foreach ($target_tables as $table) {
        $q = $pdo->prepare("DESCRIBE " . $table);
        $q->execute();
        $table_fields = $q->fetchAll(PDO::FETCH_COLUMN);
        $csv_file = '"' . implode('","', $table_fields) . '"' . "\r\n";

        $stmt = $pdo->prepare("SELECT * FROM " . $table);
        try {
            $stmt->execute();
        } catch (PDOException $e) {
            die("Can't connect to database.");
        }
        $result = $stmt->fetchAll(PDO:: FETCH_ASSOC);
        if (!empty($result)) {
            foreach ($result as $row) {
                $csv_file .= '"' . implode('","', $row) . '"' . "\r\n";
            }
        }

        $file = fopen($file_name, "a");
        fwrite($file, trim($csv_file) . "\r\n\r\n");
    }

    fclose($file);

    header('Content-type: application/csv');
    header("Content-Disposition: inline; filename=" . $file_name);
    readfile($file_name);
    unlink($file_name);
}

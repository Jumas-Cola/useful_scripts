<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="auth/css/main.css">

    <title>Экспортировать базу</title>
</head>
<body>

<div class="container mt-5">
    <div class="row">
        <div id="login_form" class="offset-md-3 col-md-6 grey-back">
            <h2 class="pt-3">
                Экспортировать базу
            </h2>
            <hr>
            <form method="GET" action="exprt_page.php">
                <div class="form-group">
                    <label for="chooseFormat">Выберите формат</label>
                    <select class="form-control" id="chooseFormat" name="t">
                        <option>SQL</option>
                        <option>CSV</option>
                    </select>
                </div>
                <div class="d-flex align-items-center">
                    <button type="submit" class="btn offset-4 col-4 text-light p-2 mt-3">
                        Экспортировать
                    </button>
                </div>
            </form>
            <div class="text-danger m-3">
                <div id="msg">
                    <?php
                    session_start();
                    if (isset($_SESSION['msg'])) {
                        echo $_SESSION['msg'];
                        unset($_SESSION['msg']);
                    }
                    ?>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        crossorigin="anonymous"></script>
<!-- Optional JavaScript -->
<script>
    $("#msg").show('slow');
    setTimeout(function () {
        $("#msg").hide('slow');
    }, 2000);
</script>
</body>
</html>
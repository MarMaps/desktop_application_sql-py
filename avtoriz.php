<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Авторизация (вход)</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h3>Авторизация: </h3>
    
    <form method="post" action="">
        <label class="" for="login">Имя пользователя (логин)</label>
        <input class="area" type="text" name="login" required> <br>

        <label class="" for="parol">Пароль</label>
        <input class="area" type="password" name="parol" required> <br>

        <input class="" name='btn' type='submit' value='Войти'>
        
    </form>

    <?php
    session_start();
    
    $con = pg_connect('host=localhost port=5432 dbname=prokat_avtomobilej user=postgres password=123456');
    
     if (isset($_POST['btn'])) {
       $login = trim($_POST['login']);
       $parol = trim($_POST['parol']);
		
       if ($login != '' && $parol != '') {
			$sql = "select id, login, parol, yr_dopyska from polzovateli
					where login = '$login'";
			$result = pg_query($con, $sql);
			$n = pg_num_rows($result);
			print "n = $n";
			if ($n == 1) {
				$user = pg_fetch_object($result);
				$_SESSION['auth'] = true;
				$_SESSION['user']['login'] = $user->login;
				$_SESSION['user']['yr_dopyska'] = $user->yr_dopyska;
				
				if ($_SESSION['user']['yr_dopyska'] == 'admin') {
					header('location: main_for_admin.php');
					exit;
				}
				elseif ($_SESSION['user']['yr_dopyska'] == 'sotrudnik') {
					header('location: main_for_sotrud.php');
					exit;
				}
				elseif ($_SESSION['user']['yr_dopyska'] == 'klient') {
					header('location: main_for_kli.php');
					exit;
				}
				
			}
			else {
				print 'неверный логин или пароль';
			}
            
		}
	 }
    
    pg_close($con);
    
    
    
    ?>
</body>
</html>
